# Steadiness Overview

<details>
<summary><b>Fixed Camera (Stable)</b></summary>


**🔵 Label Name:** `fixed_camera`  

<details>
<summary><b>🟠 Question (Definition)</b></summary>

- Is the camera completely still without any motion or shaking?  

- Is the camera completely still without any movement?  

- Does the camera remain perfectly stationary throughout?  

- Does the camera remain perfectly still throughout the shot?  

- Is the camera entirely stationary with no visible vibrations?  

- Is the camera locked off without any instability?  

- Is there absolutely no shake or motion in the camera?  

- Is the camera entirely stable with no visible shaking?  

- Is this a fixed camera shot without any shaking?  

- Is the camera locked and stationary with no signs of movement?  

- Is the camera locked in place without any motion or shaking?  

</details>

<details>
<summary><b>🟠 Alternative Question</b></summary>

- Is the camera still?  

- Is the camera stable?  

- Is the camera fixed?  

- Is the camera locked?  

- Is the camera motionless?  

- Is the camera staionary?  

- Is the camera not moving?  

- Is the camera not shaking?  

- Is the camera not vibrating?  

- Is the camera not swaying?  

- Is the camera not wobbling?  

</details>

<details>
<summary><b>🟠 Prompt (Definition)</b></summary>

- A video where the camera remains completely still with no motion or shaking.  

- A video where the camera is completely still without any movement.  

- A video where the camera remains perfectly stationary throughout.  

- A video where the camera remains perfectly still throughout the shot.  

- A video where the camera is entirely stationary with no visible vibrations.  

- A video where the camera is locked off without any instability.  

- A video where there is absolutely no shake or motion in the camera.  

- A video where the camera is entirely stable with no visible shaking.  

- A video that features a fixed camera shot without any shaking.  

- A video where the camera is locked and stationary with no signs of movement.  

- A video where the camera is locked in place without any motion or shaking.  

</details>

<details>
<summary><b>🟠 Alternative Prompt</b></summary>

- A video with a still camera.  

- A video where the camera is stable.  

- A video with a fixed camera.  

- A video where the camera is locked.  

- A video with a motionless camera.  

- A video where the camera is stationary.  

- A video where the camera is not moving.  

- A video where the camera is not shaking.  

- A video where the camera is not vibrating.  

- A video where the camera is not swaying.  

- A video where the camera is not wobbling.  

</details>

**🟢 Positive:** `self.cam_motion.steadiness in ['static'] and self.cam_motion.camera_movement in ['no']`  

**🔴 Negative:** `self.cam_motion.steadiness not in ['static']`  

<details>
<summary><b>🟠 Negative (Easy)</b></summary>

- **not_fixed_camera**: `self.cam_motion.camera_movement not in ['no']`  

</details>

<details>
<summary><b>🟠 Negative (Hard)</b></summary>

- **fixed_but_slightly_shaky**: `self.cam_motion.steadiness in ['smooth', 'unsteady'] and self.cam_motion.camera_movement in ['no']`  

</details>

</details>
