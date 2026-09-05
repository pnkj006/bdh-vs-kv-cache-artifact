# Integration Guide

This document defines how the backend and artifact integrate.

---

# Ownership

Backend Developer
- src/
- notebooks/
- data/
- docs/
- blog/
- README
- precomputed generation

Artifact Developer
- artifact/index.html
- artifact/styles.css
- artifact/app.js
- artifact/components/*
- artifact/assets/*

Do not modify each other's directories unless discussed.

---

# Backend → Artifact Contract

The artifact must NEVER implement scientific logic.

It only visualizes JSON produced by the backend.

All backend outputs are stored in

artifact/precomputed/

---

# Expected JSON Files

## memory_curve.json

```json
{
  "tokens":[128,256,512],
  "kv_memory":[0.2,0.4,0.8],
  "hebbian_memory":[0.03,0.03,0.03]
}
```

---

## simulation.json

```json
{
  "frames":[
    {
      "step":0,
      "matrix":[...],
      "norm":0.23
    }
  ]
}
```

---

## metrics.json

```json
{
    "current_step":45,
    "active_synapses":320,
    "sparsity":0.12,
    "memory_kb":14.2
}
```

---

# Data Loading

Use

```javascript
fetch("precomputed/memory_curve.json")
```

Never hardcode numerical values.

---

# Artifact Responsibilities

The artifact should

- Load JSON
- Render charts
- Render neuron heatmap
- Update UI
- Animate transitions
- Respond to controls

---

# Backend Responsibilities

The backend

- Generates simulations
- Computes memory curves
- Produces JSON
- Performs evaluations
- Maintains scientific correctness

---

# Live vs Precomputed

Live

- Slider interaction
- Heatmap animation
- UI updates

Precomputed

- Large simulations
- Memory curves
- Comparison data

---

# Integration Rules

1. Never change JSON structure without discussion.

2. Backend owns data.

3. Artifact owns presentation.

4. Keep UI and scientific code separate.

5. If additional data is required, request a new JSON field instead of embedding calculations inside the UI.

---

# Git Workflow

Main branch

main

Backend

feature/backend

Artifact

feature/artifact

Merge only after pull request review.

---

# Goal

The backend should be replaceable without modifying the frontend.

The frontend should be redesignable without modifying backend code.

Maintain a strict separation between computation and presentation.