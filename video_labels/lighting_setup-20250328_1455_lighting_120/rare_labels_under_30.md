# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Is the lighting on the subject complex (e.g., 2D/2.5D videos) or varying due to changes in lighting, camera motion, subject transitions, or multiple subjects with different lighting conditions? | 29 | 47 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex |
| Is the subject illuminated with soft, ambient light? | 25 | 22 | lighting_setup.subject_lighting.light_direction.direction_is_ambient_light |
| Does the lighting on the subject have a normal contrast ratio (1:2 to 1:8), providing a balanced distinction between bright and dark areas? | 23 | 53 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_normal |
| Does the scene in this video features hard lighting with strong, directional light? | 23 | 93 | lighting_setup.light_quality.light_quality_is_hard |
| Does the video feature bright, direct sunlight with strong intensity? | 22 | 35 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_sunny |
| Is there a noticeable light source illuminating the subject from one side (side lighting) as seen from the camera’s perspective? | 20 | 27 | lighting_setup.subject_lighting.light_direction.direction_is_side_light |
| Does the video contain practical artificial light with its source(s) clearly visible in the frame? | 20 | 96 | lighting_setup.light_source.has_artificial_practical_light |
| Is there a noticeable light source illuminating the subject from the top (top lighting) as seen from the camera’s perspective? | 19 | 28 | lighting_setup.subject_lighting.light_direction.direction_is_top_light |
| Does the lighting on the subject have a high contrast ratio, where lit areas are significantly brighter than dark areas (1:8 or above)? | 18 | 58 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_high |
| Does the video feature soft, diffused light on an overcast day? | 16 | 41 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_overcast |
| Does the scene in this video contain both hard and soft lighting? | 15 | 87 | lighting_setup.light_quality.light_quality_is_contrasting |
| Does the video feature regular daylight with balanced brightness, neither particularly hard nor soft? | 15 | 42 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_normal |
| Does the video’s brightness level change over time? | 15 | 94 | lighting_setup.color_grading.brightness.brightness_is_changing |
| Is the subject lit by low-key lighting? | 14 | 62 | lighting_setup.subject_lighting.light_contrast.low_key_lighting |
| Is the video noticeably dark or underexposed? | 14 | 102 | lighting_setup.color_grading.brightness.brightness_is_darker_than_normal |
| Does the video contain distinct shadow patterns or gobo lighting effects that shape the visual composition? | 14 | 102 | lighting_setup.shadow_pattern.has_shadow_patterns |
| Does the video feature volumetric lighting, where light appears as a visible volume? | 13 | 103 | lighting_setup.volumetric_lighting.has_volumetric_lighting |
| Does the video lacks a realistic light source, with lighting that does not follow natural physics? | 12 | 104 | lighting_setup.light_source.is_abstract |
| Does the video have strong contrast between bright and dark areas? | 12 | 97 | lighting_setup.color_grading.brightness.brightness_is_contrasting |
| Is the video predominantly dark with dim lighting but not so underexposed that most details are lost? | 12 | 104 | lighting_setup.color_grading.brightness.brightness_is_dark |
| Is the video set in a synthetic or 2D environment with unrealistic lighting effects? | 12 | 104 | lighting_setup.scene.scene_type_is_synthetic |
| Is the video noticeably bright or overexposed? | 11 | 105 | lighting_setup.color_grading.brightness.brightness_is_brighter_than_normal |
| Is the video well-lit with strong lighting, making the scene bright and clear but not overexposed? | 11 | 105 | lighting_setup.color_grading.brightness.brightness_is_bright |
| Does the lighting in the video flash, creating sudden bursts of light in an on/off pattern? | 10 | 106 | lighting_setup.dynamic_light.flashing |
| Does the lighting setup create a polished, professional appearance, common in portrait photography or videography? | 9 | 107 | lighting_setup.subject_lighting.portrait_lighting |
| Does the light quality in the scene change between hard and soft over time? | 9 | 93 | lighting_setup.light_quality.light_quality_is_changing |
| Does the video mainly feature highly saturated colors, making hues appear vivid and intense? | 9 | 107 | lighting_setup.color_grading.saturation.color_saturation_is_high |
| Does the video mainly feature desaturated colors, making hues appear muted or grayish? | 9 | 107 | lighting_setup.color_grading.saturation.color_saturation_is_low |
| Is the video predominantly featuring cool colors, such as blues or greens? | 9 | 107 | lighting_setup.color_grading.temperature.color_temperature_is_cool |
| Is the scene type unclear, ambiguous, or changing throughout the video? | 9 | 107 | lighting_setup.scene.scene_type_is_complex_others |
| Is there a noticeable light source illuminating the subject from behind (backlighting) as seen from the camera’s perspective? | 8 | 39 | lighting_setup.subject_lighting.light_direction.direction_is_back_light |
| Is there a noticeable light source illuminating the subject from the front as seen from the camera’s perspective? | 8 | 39 | lighting_setup.subject_lighting.light_direction.direction_is_front_light |
| Does the video contain a revealing shot that gradually uncovers a new environment or subject? | 8 | 108 | lighting_setup.dynamic_effect.revealing_shot |
| Does the primary light source in the video change over time or include a rare light source that is not the sun, fire, moon and stars, or artificial light? | 8 | 108 | lighting_setup.light_source.has_complex_light_source |
| Does the video feature a complex color composition or dynamics that cannot be classified as strictly black-and-white, warm, cool, or neutral? | 8 | 108 | lighting_setup.color_grading.temperature.color_temperature_is_complex_others |
| Does the video feature a noticeable reflection from light bouncing off a smooth, glossy surface but does not clearly mirror the scene in detail? | 7 | 109 | lighting_setup.reflection.reflection_from_glossy_surface |
| Does the video feature lighting that varies in brightness, either through rhythmic pulsing or irregular flickering? | 7 | 109 | lighting_setup.dynamic_light.pulsing_flickering |
| Does the video feature major light source(s) that traverse the scene or change direction? | 7 | 109 | lighting_setup.dynamic_light.moving_light |
| Does the video feature strong contrasts between warm and cool colors? | 7 | 101 | lighting_setup.color_grading.temperature.color_temperature_is_contrasting |
| Does the video have a highly complex or unusual brightness level that is hard to classify? | 7 | 109 | lighting_setup.color_grading.brightness.brightness_is_complex_others |
| Does the video feature shadows shaped by the subject, emphasizing form or movement? | 7 | 109 | lighting_setup.shadow_pattern.subject_shape |
| Is the subject lit with flat lighting, with little to no contrast? | 6 | 70 | lighting_setup.subject_lighting.light_contrast.flat_lighting |
| Does the lighting on the subject have minimal contrast (1:1 to 1:2), creating a flat lighting effect? | 6 | 70 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_minimal |
| Is the subject illuminated by a mix of back and side lighting? | 6 | 41 | lighting_setup.subject_lighting.light_direction.direction_is_rear_side |
| Does the video feature visible splashing or wave-like motion in water or other liquids? | 6 | 110 | lighting_setup.dynamic_effect.splashing_waves |
| Does the video have noticeable shifts in color saturation between high and low over time? | 6 | 106 | lighting_setup.color_grading.saturation.color_saturation_is_changing |
| Does the video have noticeable shifts between warm and cool color tones? | 6 | 102 | lighting_setup.color_grading.temperature.color_temperature_is_changing |
| Does the video feature distinct or dynamic shadow patterns or gobo lighting effects other than Venetian blinds, window frames, foliage, or the subject's shape? | 6 | 110 | lighting_setup.shadow_pattern.shadow_patterns_gobo_others |
| Does the video feature artificial colored or neon lighting? | 6 | 110 | lighting_setup.special_effect.colored_neon_lighting |
| Is the video predominantly featuring warm colors, such as reds, oranges, or yellows? | 5 | 111 | lighting_setup.color_grading.temperature.color_temperature_is_warm |
| Does the video feature volumetric lighting with a well-defined, contained shape (other than beams, god rays, or spotlights)? | 5 | 111 | lighting_setup.volumetric_lighting.volumetric_light_others |
| Does the video feature a vignette effect, where the edges gradually darken or fade? | 5 | 111 | lighting_setup.special_effect.vignette |
| Is there a silhouette lighting effect that creates a dark outline of the foreground subject against a bright background? | 5 | 111 | lighting_setup.special_effect.silhouette |
| Does the video include shot transitions? | 4 | 116 | lighting_setup.has_shot_transition_lighting_setup |
| Does the video feature warm, golden sunlight at sunrise or sunset? | 4 | 53 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_sunset_sunrise |
| Is the video entirely in black and white, with no color present? | 4 | 112 | lighting_setup.color_grading.is_black_white |
| Does the video feature a complex color composition or dynamics that cannot be classified as strictly high, low, or neutral color saturation? | 4 | 112 | lighting_setup.color_grading.saturation.color_saturation_is_complex_others |
| Does the video feature intense light passing through smoke, fog, or liquid, shaping visible light volumes? | 4 | 112 | lighting_setup.volumetric_lighting.light_through_medium |
| Is there rim lighting that creates a glowing edge around the subject? | 4 | 112 | lighting_setup.special_effect.rim_light |
| Is the subject illuminated by a mix of front and side lighting? | 3 | 44 | lighting_setup.subject_lighting.light_direction.direction_is_front_side |
| Does the video feature a noticeable aerial perspective, where distant scenery appears less detailed, desaturated, and hazier due to atmospheric effects? | 3 | 113 | lighting_setup.natural_effect.aerial_perspective |
| Does the video show objects or characters floating or levitating as if unaffected by gravity? | 3 | 113 | lighting_setup.dynamic_effect.levitation_floating |
| Does the video feature a visible diffusion effect, where particles, fluids, or other materials spread and disperse over time? | 3 | 113 | lighting_setup.dynamic_effect.diffusion |
| Does the video contain obvious lens flares? | 3 | 113 | lighting_setup.lens_effect.lens_flares |
| Does the video show noticeable shimmering effects or bright highlights from light reflecting off water? | 2 | 114 | lighting_setup.reflection.reflection_from_water |
| Does the lighting color in the video change abruptly and rapidly (a sudden color shift)? | 2 | 114 | lighting_setup.dynamic_light.color_shifting_sudden |
| Does the lighting color in the video change gradually and smoothly (a smooth color shift)? | 2 | 114 | lighting_setup.dynamic_light.color_shifting_smooth |
| Does the video capture a lightning effect with intense flashes and jagged, branching streaks? | 2 | 114 | lighting_setup.natural_effect.lightning |
| Does the video feature an explosion with a sudden burst of flames, matter, and outward force? | 2 | 114 | lighting_setup.dynamic_effect.explosion |
| Does the video feature a transformation or morphing effect where one object changes into another? | 2 | 114 | lighting_setup.dynamic_effect.transformation_morphing |
| Is the video primarily lit by firelight? | 2 | 114 | lighting_setup.light_source.has_firelight |
| Is the video extremely dark and underexposed, with barely any visible details due to minimal lighting? | 2 | 114 | lighting_setup.color_grading.brightness.brightness_is_very_dark |
| Does the video feature visible beams of light with well-defined edges, creating linear volumes of light? | 2 | 114 | lighting_setup.volumetric_lighting.volumetric_beam_light |
| Does the video feature striking, separated rays of light (god rays) streaming through gaps in the environment? | 2 | 114 | lighting_setup.volumetric_lighting.god_rays |
| Does the video feature shadows cast by window frames? | 2 | 114 | lighting_setup.shadow_pattern.window_frames |
| Does the video feature shadow patterns created by foliage, such as leaves or branches? | 2 | 114 | lighting_setup.shadow_pattern.foliage |
| Does the video contain typical lens flares, appearing as circular, polygonal, veiling, scattered, or streak-like artifacts? | 2 | 114 | lighting_setup.lens_effect.lens_flare_regular |
| Does the video feature light from street lamps? | 2 | 114 | lighting_setup.special_effect.street_light |
| Does the video feature water caustics, where light creates dynamic rippling patterns? | 2 | 114 | lighting_setup.special_effect.water_caustics |
| Does the video feature bright and colorful city lighting from various artificial sources? | 2 | 114 | lighting_setup.special_effect.city_light |
| Is there Rembrandt lighting that illuminates one side of the subject’s face, creating a small triangle of light on the other? | 1 | 115 | lighting_setup.subject_lighting.rembrandt_lighting |
| Is there a noticeable light source illuminating the subject from below (bottom lighting) as seen from the camera’s perspective? | 1 | 46 | lighting_setup.subject_lighting.light_direction.direction_is_bottom_light |
| Does the video show strong reflections from light bouncing off a mirror, clearly mirroring the scenery in detail? | 1 | 115 | lighting_setup.reflection.reflection_from_mirror |
| Does the video show objects breaking, shattering, or fragmenting into smaller pieces? | 1 | 115 | lighting_setup.dynamic_effect.shattering_breaking |
| Does the video feature concentrated, cone-shaped volumes of light? | 1 | 115 | lighting_setup.volumetric_lighting.volumetric_spot_light |
| Does the video feature distinct shadow patterns cast by venetian blinds? | 1 | 115 | lighting_setup.shadow_pattern.venetian_blinds |
| Does the video use a mist diffusion filter to soften the image, creating a dreamy, glowing effect? | 1 | 115 | lighting_setup.lens_effect.mist_diffusion |
| Does the video feature soft, out-of-focus light orbs in the background, created by distant lights and a shallow depth of field? | 1 | 115 | lighting_setup.lens_effect.bokeh |
| Does the video contain anamorphic lens flares as bright, elongated streaks from light interacting with an anamorphic lens? | 1 | 115 | lighting_setup.lens_effect.lens_flares_anamorphic |
| Is the subject lit with high-key lighting? | 0 | 76 | lighting_setup.subject_lighting.light_contrast.high_key_lighting |
| Does the video feature a noticeable heat haze effect, with air distortions and shimmering caused by rising heat? | 0 | 116 | lighting_setup.natural_effect.heat_haze |
| Does the video feature an aurora, with flowing, colorful light patterns in the sky? | 0 | 116 | lighting_setup.natural_effect.aurora |
| Does the video feature a noticeable rainbow? | 0 | 116 | lighting_setup.natural_effect.rainbow |
| Is the video lit by moonlight or starnight, with the moon or stars visible? | 0 | 116 | lighting_setup.light_source.has_moonlight_starlight |
| Does the video feature strong contrasts between highly saturated and desaturated hues? | 0 | 112 | lighting_setup.color_grading.saturation.color_saturation_is_contrasting |
| Is the video excessively bright and overexposed, making details hard to see? | 0 | 116 | lighting_setup.color_grading.brightness.brightness_is_very_bright |
| Does the video feature a headlight or flashlight that illuminates the scene in front with intense, focused light, creating sharp contrast against darker surroundings? | 0 | 116 | lighting_setup.special_effect.headlight_flashlight |
