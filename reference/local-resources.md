# Local resources

Criteria LOCAL-01/02 and PWA-08. Configure against the actual host rather than an assumed personal machine. No local vision-model performance or memory benchmark is supplied.

Browsers, development servers, compilers, screenshot comparison, accessibility scans, video encoding, simulators and optional local vision models share resources. Start with one worker. Measure OS memory pressure, process RSS, runtime, warm/cold behavior, image resolution, context length and quantization. On macOS, `memory_pressure` and `vm_stat` can help; use equivalent tools on other systems. Inspect only your test processes.

A parameter-count estimate covers weights only: roughly parameters × bits / 8 bytes, before activations, context/KV caches and runtime overhead. It is not a total-memory guarantee. Reduce concurrency if swapping/pressure persists. Isolate capture/performance runs from compilation, encoding and inference load.

Evaluate optional local vision on labeled defects such as clipping, focus, obscured safe areas and missing states. Choose by predefined recall, false positives, license and measured load, not attractive prose or model size. [MLX-VLM](https://github.com/Blaizzy/mlx-vlm) is an Apple-Silicon candidate, not a required cross-platform dependency.

Simulators use host resources. Validate touch latency, thermal behavior, haptics, energy and high-refresh performance on actual supported devices. A desktop recording does not prove mobile display performance. Hosted vision is optional within the existing project's data/permission constraints.
