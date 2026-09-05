document.addEventListener('DOMContentLoaded', () => {
  const contextSlider = document.getElementById('context-length');
  const contextVal = document.getElementById('context-length-val');
  const modeToggles = document.getElementsByName('mode');

  const kvMemory = document.getElementById('kv-memory');
  const kvBar = document.getElementById('kv-bar');
  const hebbianMemory = document.getElementById('hebbian-memory');
  const hebbianBar = document.getElementById('hebbian-bar');

  const equationDisplay = document.getElementById('equation-display');

  const canvas = document.getElementById('neuron-grid');
  const ctx = canvas.getContext('2d');
  const sparsitySlider = document.getElementById('sparsity');
  const sparsityVal = document.getElementById('sparsity-val');
  const decaySlider = document.getElementById('decay');
  const decayVal = document.getElementById('decay-val');

  const stepBtn = document.getElementById('step-btn');
  const runNBtn = document.getElementById('run-n-btn');
  const resetBtn = document.getElementById('reset-btn');
  const normVal = document.getElementById('norm-val');

  let currentMode = 'kv';
  const MAX_CONTEXT = 131072;
  const BYTES_PER_TOKEN_KV = 131072;
  const HEBBIAN_FIXED_BYTES = 8388608;

  const MATRIX_SIZE = 32;
  let synapticMatrix = new Float32Array(MATRIX_SIZE * MATRIX_SIZE);

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0.00 GiB';
    const k = 1024;
    if (bytes < k * k) return (bytes / k).toFixed(2) + ' KiB';
    if (bytes < k * k * k) return (bytes / (k * k)).toFixed(2) + ' MiB';
    return (bytes / (k * k * k)).toFixed(2) + ' GiB';
  };

  const updateEquations = () => {
    if (currentMode === 'kv') {
      equationDisplay.innerHTML = `
        <div>KV Memory = 2 &times; L &times; H<sub>kv</sub> &times; d<sub>h</sub> &times; 2 bytes &times; seq_len</div>
        <span class="equation-source">Exact formula for standard Multi-Query / GQA Transformer.</span>
      `;
    } else {
      equationDisplay.innerHTML = `
        <div>&Delta;W = &gamma;W + (1 - &gamma;) x x<sup>T</sup></div>
        <span class="equation-source">Simplified pedagogical proxy. See <a href="https://arxiv.org/abs/2509.26507" target="_blank">Kosowski et al. 2025, Table 1</a> for the formal "equations of reasoning" and thermodynamic bound statement.</span>
      `;
    }
  };

  const updateMemoryFootprint = () => {
    const tokens = parseInt(contextSlider.value);
    contextVal.textContent = tokens.toLocaleString() + ' tokens';

    const kvBytes = tokens * BYTES_PER_TOKEN_KV;
    kvMemory.textContent = formatBytes(kvBytes);
    const maxKvBytes = MAX_CONTEXT * BYTES_PER_TOKEN_KV;
    const kvPercent = (kvBytes / maxKvBytes) * 100;
    kvBar.style.width = `${Math.min(kvPercent, 100)}%`;

    hebbianMemory.textContent = '8192 KiB';
    const hebbianPercent = (HEBBIAN_FIXED_BYTES / maxKvBytes) * 100;
    hebbianBar.style.width = `${Math.max(hebbianPercent, 2)}%`;

    kvBar.parentElement.parentElement.style.opacity = currentMode === 'kv' ? '1' : '0.45';
    hebbianBar.parentElement.parentElement.style.opacity = currentMode === 'hebbian' ? '1' : '0.45';
  };

  const drawMatrix = () => {
    let maxVal = 0;
    for (let i = 0; i < synapticMatrix.length; i++) {
      maxVal = Math.max(maxVal, Math.abs(synapticMatrix[i]));
    }
    if (maxVal === 0) maxVal = 1;

    const cellW = canvas.width / MATRIX_SIZE;
    const cellH = canvas.height / MATRIX_SIZE;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < MATRIX_SIZE; i++) {
      for (let j = 0; j < MATRIX_SIZE; j++) {
        const val = synapticMatrix[i * MATRIX_SIZE + j];
        const normalized = val / maxVal;
        
        let r, g, b;
        if (normalized > 0) {
          const t = normalized;
          r = Math.round(250 - t * (250 - 58)); 
          g = Math.round(248 - t * (248 - 90)); 
          b = Math.round(242 - t * (242 - 53));
        } else {
          const t = -normalized;
          r = Math.round(250 - t * (250 - 166)); 
          g = Math.round(248 - t * (248 - 64)); 
          b = Math.round(242 - t * (242 - 45));
        }
        
        ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
        ctx.fillRect(j * cellW, i * cellH, Math.ceil(cellW), Math.ceil(cellH));
      }
    }
  };

  const calcNorm = () => {
    let sumSq = 0;
    for (let i = 0; i < synapticMatrix.length; i++) sumSq += synapticMatrix[i] * synapticMatrix[i];
    return Math.sqrt(sumSq);
  };

  const updateNormDisplay = () => {
    const norm = calcNorm();
    normVal.textContent = norm.toFixed(2);
    if (norm > 100) {
      normVal.classList.add('diverging');
      normVal.title = "Unbounded growth detected! This shows why the decay parameter is critical to keeping the state bounded.";
    } else {
      normVal.classList.remove('diverging');
      normVal.title = "";
    }
  };

  const stepSimulation = () => {
    const sparsity = parseInt(sparsitySlider.value) / 100;
    const decay = parseFloat(decaySlider.value);

    const x = new Float32Array(MATRIX_SIZE);
    for (let i = 0; i < MATRIX_SIZE; i++) {
      if (Math.random() < sparsity) x[i] = (Math.random() * 2) - 1;
    }

    for (let i = 0; i < MATRIX_SIZE; i++) {
      for (let j = 0; j < MATRIX_SIZE; j++) {
        const idx = i * MATRIX_SIZE + j;
        synapticMatrix[idx] = (1 - decay) * synapticMatrix[idx] + (x[i] * x[j]);
      }
    }

    drawMatrix();
    updateNormDisplay();
  };

  contextSlider.addEventListener('input', updateMemoryFootprint);

  modeToggles.forEach(toggle => {
    toggle.addEventListener('change', (e) => {
      currentMode = e.target.value;
      updateEquations();
      updateMemoryFootprint();
    });
  });

  sparsitySlider.addEventListener('input', (e) => { sparsityVal.textContent = e.target.value + '%'; });
  decaySlider.addEventListener('input', (e) => { decayVal.textContent = parseFloat(e.target.value).toFixed(2); });

  stepBtn.addEventListener('click', stepSimulation);

  runNBtn.addEventListener('click', () => {
    let steps = 0;
    const maxSteps = 150;
    runNBtn.disabled = true;
    stepBtn.disabled = true;
    const interval = setInterval(() => {
      stepSimulation();
      steps++;
      if (steps >= maxSteps) {
        clearInterval(interval);
        runNBtn.disabled = false;
        stepBtn.disabled = false;
      }
    }, 16);
  });

  resetBtn.addEventListener('click', () => {
    synapticMatrix = new Float32Array(MATRIX_SIZE * MATRIX_SIZE);
    drawMatrix();
    updateNormDisplay();
  });

  updateEquations();
  updateMemoryFootprint();
  drawMatrix();
  updateNormDisplay();
});
