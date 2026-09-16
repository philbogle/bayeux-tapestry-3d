# Bayeux Tapestry 3D Walkthrough

**[Experience the interactive 3D tapestry here](https://philbogle.github.io/bayeux-tapestry-3d/)**

A browser-based 3D walkthrough visualization of the Bayeux Tapestry, navigable via keyboard shortcuts or touch gestures. 

This project builds on and is complementary to the high-resolution Bayeux Tapestry online experience provided by the [British Museum](https://www.britishmuseum.org/bayeux-tapestry-online-experience). It uses their high-resolution .webp image tiles and renders them in a continuous 3D space using [Three.js](https://threejs.org/). This allows you to smoothly "walk" alongside the entire tapestry and tilt your perspective to look ahead.

### Features
* **Continuous 3D Navigation**: Pan across the 224-foot tapestry using momentum-based physics.
* **Variable Level of Detail (LOD)**: The system manages three tiers of image resolution based on zoom depth and camera speed. A base layer handles panning across the canvas. When you stop moving and zoom in close, the engine fetches 2x and 4x resolution textures, allowing you to inspect individual stitches while managing device memory.
* **Interactive Supertitles**: English translations hover over the Latin script, fading out during fast camera movements to reduce visual clutter.
* **Cross-Platform**: Support for desktop and mobile, including trackpads, scroll wheels, and touch gestures.

### Controls
* **Left/Right Arrows, A/D, or Scroll/Swipe**: Walk along the tapestry. Continuous movement builds momentum and tilts the camera to adjust the viewing angle.
* **Up/Down Arrows, W/S, or Pinch**: Move closer to or further away from the tapestry.

### Acknowledgements
Thanks to the British Museum, the City of Bayeux, and their partners for digitizing the tapestry and making it available for fair use.

### License
This project's source code is freely available under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.
