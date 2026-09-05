document.addEventListener("DOMContentLoaded", async () => {

  // ==========================================================
  // Load backend-generated JSON
  // ==========================================================
  try {
    const [memoryCurve, simulationData, metrics] = await Promise.all([
      fetch("precomputed/memory_curve.json").then(r => r.json()),
      fetch("precomputed/simulation.json").then(r => r.json()),
      fetch("precomputed/metrics.json").then(r => r.json())
    ]);

    // ==========================================================
    // DOM Elements
    // ==========================================================

    const contextSlider = document.getElementById("context-length");
    const contextVal = document.getElementById("context-length-val");

    const modeToggles = document.getElementsByName("mode");

    const kvMemory = document.getElementById("kv-memory");
    const kvBar = document.getElementById("kv-bar");

    const hebbianMemory = document.getElementById("hebbian-memory");
    const hebbianBar = document.getElementById("hebbian-bar");

    const equationDisplay = document.getElementById("equation-display");

    const canvas = document.getElementById("neuron-grid");
    const ctx = canvas.getContext("2d");

    const sparsitySlider = document.getElementById("sparsity");
    const sparsityVal = document.getElementById("sparsity-val");

    const decaySlider = document.getElementById("decay");
    const decayVal = document.getElementById("decay-val");

    const stepBtn = document.getElementById("step-btn");
    const runNBtn = document.getElementById("run-n-btn");
    const resetBtn = document.getElementById("reset-btn");

    const normVal = document.getElementById("norm-val");

    // ==========================================================
    // Application State
    // ==========================================================

    let currentMode = "kv";

    let currentFrame = 0;

    const MATRIX_SIZE =
      simulationData.frames[0].matrix.length;

    let synapticMatrix =
      simulationData.frames[0].matrix;

    const MAX_CONTEXT =
      memoryCurve.tokens[memoryCurve.tokens.length - 1];

    const MAX_KV_MEMORY =
      memoryCurve.kv_memory[memoryCurve.kv_memory.length - 1];

    const FIXED_HEBBIAN_MEMORY =
      memoryCurve.hebbian_memory[0];

    // ==========================================================
    // Helpers
    // ==========================================================

    function nearestTokenIndex(tokens) {

      let idx = 0;

      let best = Infinity;

      for (let i = 0; i < memoryCurve.tokens.length; i++) {

        const d =
          Math.abs(memoryCurve.tokens[i] - tokens);

        if (d < best) {

          best = d;

          idx = i;

        }

      }

      return idx;

    }

    function formatGiB(value) {

      return value.toFixed(2) + " GiB";

    }

    function formatKiB(value) {

      return value.toFixed(0) + " KiB";

    }
    // ==========================================================
    // Equation Display
    // ==========================================================

    function updateEquations() {

      if (currentMode === "kv") {

        equationDisplay.innerHTML = `
        <div>
          KV Memory =
          2 × L × H<sub>kv</sub> × d<sub>h</sub>
          × 2 bytes × seq_len
        </div>

        <span class="equation-source">
          Exact Transformer KV-cache memory formula.
        </span>
      `;

      } else {

        equationDisplay.innerHTML = `
        <div>
          ΔW = γW + (1 − γ)xx<sup>T</sup>
        </div>

        <span class="equation-source">
          Simplified pedagogical Hebbian update.
          See Kosowski et al. (2025).
        </span>
      `;

      }

    }

    // ==========================================================
    // Memory Panel
    // ==========================================================

    function updateMemoryFootprint() {

      const tokens =
        parseInt(contextSlider.value);

      contextVal.textContent =
        tokens.toLocaleString() + " tokens";

      const idx =
        nearestTokenIndex(tokens);

      const kv =
        memoryCurve.kv_memory[idx];

      const hebb =
        memoryCurve.hebbian_memory[idx];

      kvMemory.textContent =
        formatGiB(kv);

      hebbianMemory.textContent =
        formatKiB(hebb);

      const kvPercent =
        (kv / MAX_KV_MEMORY) * 100;

      kvBar.style.width =
        `${kvPercent}%`;

      const hebbPercent =
        Math.max(
          (hebb / MAX_KV_MEMORY) * 100,
          2
        );

      hebbianBar.style.width =
        `${hebbPercent}%`;

      kvBar.parentElement.parentElement.style.opacity =
        currentMode === "kv"
          ? "1"
          : "0.45";

      hebbianBar.parentElement.parentElement.style.opacity =
        currentMode === "hebbian"
          ? "1"
          : "0.45";

    }
    // ==========================================================
    // Heatmap Renderer
    // ==========================================================

    function resizeCanvas() {
      const rect = canvas.parentElement.getBoundingClientRect();

      canvas.width = rect.width;
      canvas.height = rect.height;
    }

    function drawMatrix() {

      let maxVal = 0;

      for (let i = 0; i < MATRIX_SIZE; i++) {

        for (let j = 0; j < MATRIX_SIZE; j++) {

          maxVal = Math.max(
            maxVal,
            Math.abs(synapticMatrix[i][j])
          );

        }

      }

      if (maxVal === 0) maxVal = 1;

      const cellW = canvas.width / MATRIX_SIZE;
      const cellH = canvas.height / MATRIX_SIZE;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < MATRIX_SIZE; i++) {

        for (let j = 0; j < MATRIX_SIZE; j++) {

          const value = synapticMatrix[i][j];

          const normalized = value / maxVal;

          let r, g, b;

          if (normalized >= 0) {

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

          ctx.fillStyle = `rgb(${r},${g},${b})`;

          ctx.fillRect(

            j * cellW,

            i * cellH,

            Math.ceil(cellW),

            Math.ceil(cellH)

          );

        }

      }

    }

    // ==========================================================
    // Frame Loader
    // ==========================================================

    function loadFrame(index) {

      if (index < 0) index = 0;

      if (index >= simulationData.frames.length)
        index = simulationData.frames.length - 1;

      currentFrame = index;

      synapticMatrix =
        simulationData.frames[currentFrame].matrix;

      normVal.textContent =
        simulationData.frames[currentFrame].norm.toFixed(2);

      if (
        simulationData.frames[currentFrame].norm > 100
      ) {

        normVal.classList.add("diverging");

        normVal.title =
          "Unbounded growth detected.";

      } else {

        normVal.classList.remove("diverging");

        normVal.title = "";

      }
      
      resizeCanvas()
      drawMatrix();

    }
    // ==========================================================
    // Simulation Controls
    // ==========================================================

    function stepSimulation() {

      if (currentFrame < simulationData.frames.length - 1) {

        loadFrame(currentFrame + 1);

      }

    }

    function resetSimulation() {

      loadFrame(0);

    }

    function runSimulation() {

      runNBtn.disabled = true;
      stepBtn.disabled = true;

      const targetFrame = Math.floor(
        (parseInt(contextSlider.value) / MAX_CONTEXT) *
        (simulationData.frames.length - 1)
      );

      const interval = setInterval(() => {

        if (currentFrame >= targetFrame) {

          clearInterval(interval);

          runNBtn.disabled = false;
          stepBtn.disabled = false;

          return;

        }

        loadFrame(currentFrame + 1);

      }, 16);

    }

    // ==========================================================
    // Button Events
    // ==========================================================

    stepBtn.addEventListener(
      "click",
      stepSimulation
    );

    runNBtn.addEventListener(
      "click",
      runSimulation
    );

    resetBtn.addEventListener(
      "click",
      resetSimulation
    );
    // ==========================================================
    // Slider Events
    // ==========================================================

    contextSlider.addEventListener("input", () => {

      updateMemoryFootprint();

    });

    sparsitySlider.addEventListener("input", (e) => {

      sparsityVal.textContent =
        e.target.value + "%";

    });

    decaySlider.addEventListener("input", (e) => {

      decayVal.textContent =
        parseFloat(e.target.value).toFixed(2);

    });

    // ==========================================================
    // Mode Toggle
    // ==========================================================

    modeToggles.forEach(toggle => {

      toggle.addEventListener("change", (e) => {

        currentMode = e.target.value;

        updateEquations();

        updateMemoryFootprint();

      });

    });

    // ==========================================================
    // Initialize Dashboard
    // ==========================================================

    updateEquations();

    updateMemoryFootprint();

    loadFrame(0);

    // ==========================================================
    // Show Backend Metrics
    // ==========================================================

    console.log("Loaded backend metrics:");

    console.table(metrics);

    console.log(
      `Tokens Processed: ${metrics.tokens_processed}`
    );

    console.log(
      `Final Norm: ${metrics.final_norm}`
    );

    console.log(
      `Active Synapses: ${metrics.active_synapses}`
    );
  } catch (err) {

    console.error("Failed to initialize application:", err);

    document.body.innerHTML = `
        <div style="
            padding:40px;
            font-family:Arial,sans-serif;
            text-align:center;
        ">
            <h2>Failed to load backend data.</h2>
            <p>
                Make sure the following files exist:
            </p>

            <ul style="display:inline-block;text-align:left">
                <li>precomputed/memory_curve.json</li>
                <li>precomputed/simulation.json</li>
                <li>precomputed/metrics.json</li>
            </ul>

            <p>Check the browser console (F12) for details.</p>
        </div>
      `;

  }

});