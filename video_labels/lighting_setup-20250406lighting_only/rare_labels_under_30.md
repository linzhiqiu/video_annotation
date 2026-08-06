# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the lighting in the video flash, creating sudden bursts of light in an on/off pattern? | 28 | 214 | lighting_setup.dynamic_light.flashing |
| Does the video feature major light source(s) that traverse the scene or change direction? | 28 | 214 | lighting_setup.dynamic_light.moving_light |
| Is the video noticeably dark or underexposed? | 28 | 214 | lighting_setup.color_grading.brightness.brightness_is_darker_than_normal |
| Is there a noticeable light source consistently illuminating the subject from the front as seen from the camera’s perspective? | 26 | 84 | lighting_setup.subject_lighting.light_direction.direction_is_front_light |
| Is the video showing a scene with predominantly dim lighting, but some details remain visible and are not completely underexposed? | 26 | 216 | lighting_setup.color_grading.brightness.brightness_is_dark |
| Is there a noticeable light source consistently illuminating the subject from behind (backlighting) as seen from the camera’s perspective? | 24 | 85 | lighting_setup.subject_lighting.light_direction.direction_is_back_light |
| Does the video feature lighting that varies in brightness, either through rhythmic pulsing or irregular flickering? | 21 | 221 | lighting_setup.dynamic_light.pulsing_flickering |
| Does the video feature a noticeable specular reflection from light bouncing off a smooth, glossy surface but does not clearly mirror the scene in detail? | 20 | 222 | lighting_setup.reflection.reflection_from_glossy_surface |
| Does the overall brightness of the video change over time, with noticeable shifts between brighter and darker levels across large portions of the frame? | 20 | 162 | lighting_setup.color_grading.brightness.brightness_is_changing |
| Does the video feature concentrated, cone-shaped volumes of light? | 19 | 223 | lighting_setup.volumetric_lighting.volumetric_spot_light |
| Is firelight a primary light source in the video? | 18 | 224 | lighting_setup.light_source.has_firelight |
| Does the primary light source in the video change over time or include a rare light source that is not the sun, fire, moon and stars, or artificial light? | 18 | 224 | lighting_setup.light_source.has_complex_light_source |
| Does the video feature intense light passing through smoke, fog, or liquid, shaping visible light volumes? | 18 | 224 | lighting_setup.volumetric_lighting.light_through_medium |
| Is the video set in a synthetic or 2D environment with unrealistic lighting effects? | 18 | 224 | lighting_setup.scene.scene_type_is_synthetic |
| Does the video feature soft, diffused sunlight from overcast skies or during blue hour? | 17 | 75 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_overcast |
| Does the video mainly feature highly saturated colors, making hues appear vivid and intense? | 16 | 226 | lighting_setup.color_grading.saturation.color_saturation_is_high |
| Is there rim lighting that creates a glowing edge around the subject? | 16 | 226 | lighting_setup.special_effect.rim_light |
| Does the video contain a revealing shot that gradually uncovers a new environment or subject? | 15 | 227 | lighting_setup.dynamic_effect.revealing_shot |
| Does the video feature a noticable diffusion effect, where particles, fluids, or other materials spread and disperse over time? | 15 | 227 | lighting_setup.dynamic_effect.diffusion |
| Does the video lacks a realistic light source, with lighting that does not follow natural physics? | 15 | 227 | lighting_setup.light_source.is_abstract |
| Does the video mainly feature desaturated colors, making hues appear muted or grayish? | 15 | 227 | lighting_setup.color_grading.saturation.color_saturation_is_low |
| Is the video predominantly featuring cool colors, such as blues or greens? | 15 | 227 | lighting_setup.color_grading.temperature.color_temperature_is_cool |
| Is the video noticeably bright or overexposed? | 15 | 227 | lighting_setup.color_grading.brightness.brightness_is_brighter_than_normal |
| Is the video showing a bright and well-lit scene, with high light levels and clearly visible details without much overexposure? | 15 | 227 | lighting_setup.color_grading.brightness.brightness_is_bright |
| Does the lighting color in the video change abruptly and rapidly (a sudden color shift)? | 14 | 228 | lighting_setup.dynamic_light.color_shifting_sudden |
| Does the video feature strong contrasts between warm and cool colors? | 13 | 160 | lighting_setup.color_grading.temperature.color_temperature_is_contrasting |
| Does the video feature distinct or dynamic shadow patterns or gobo lighting effects other than Venetian blinds, window frames, foliage, or the subject's shape? | 13 | 229 | lighting_setup.shadow_pattern.shadow_patterns_gobo_others |
| Does the video contain obvious lens flares? | 13 | 229 | lighting_setup.lens_effect.lens_flares |
| Does the video feature volumetric lighting with a well-defined, contained shape (other than beams, god rays, or spotlights)? | 12 | 230 | lighting_setup.volumetric_lighting.volumetric_light_others |
| Is the subject consistently illuminated by a mix of front and side lighting? | 11 | 96 | lighting_setup.subject_lighting.light_direction.direction_is_front_side |
| Does the light quality in the scene change between hard and soft over time? | 11 | 172 | lighting_setup.light_quality.light_quality_is_changing |
| Does the video feature an explosion with a sudden burst of flames, matter, and outward force? | 11 | 231 | lighting_setup.dynamic_effect.explosion |
| Does the video feature striking, separated rays of light (god rays) streaming through gaps in the environment? | 11 | 231 | lighting_setup.volumetric_lighting.god_rays |
| Does the video feature shadows shaped by the subject to support the narrative, emphasizing form or movement? | 11 | 231 | lighting_setup.shadow_pattern.subject_shape |
| Does the video feature shadow patterns created by foliage, such as leaves or branches? | 11 | 231 | lighting_setup.shadow_pattern.foliage |
| Does the video feature soft, out-of-focus light orbs in the background, created by distant lights and a shallow depth of field? | 11 | 231 | lighting_setup.lens_effect.bokeh |
| Does the video contain typical (non-anamorphic) lens flares, appearing as circular, polygonal, veiling, scattered, or streak-like artifacts? | 10 | 232 | lighting_setup.lens_effect.lens_flare_regular |
| Does the video feature a vignette effect, where the edges gradually darken or fade? | 10 | 232 | lighting_setup.special_effect.vignette |
| Is the subject lit with flat lighting, with little to no contrast? | 9 | 175 | lighting_setup.subject_lighting.light_contrast.flat_lighting |
| Does the lighting on the subject have minimal contrast ratio, creating a flat lighting effect (e.g., 1:1 to 1:2)? | 9 | 175 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_minimal |
| Is the subject lit with high-key lighting? | 9 | 175 | lighting_setup.subject_lighting.light_contrast.high_key_lighting |
| Does the video show objects or characters floating or levitating as if unaffected by gravity? | 9 | 233 | lighting_setup.dynamic_effect.levitation_floating |
| Does the video show noticeable splashing or wave-like movement in liquid? | 9 | 233 | lighting_setup.dynamic_effect.splashing_waves |
| Does the video have noticeable shifts between warm and cool color tones? | 9 | 164 | lighting_setup.color_grading.temperature.color_temperature_is_changing |
| Is the subject consistently illuminated by a mix of back and side lighting? | 8 | 94 | lighting_setup.subject_lighting.light_direction.direction_is_rear_side |
| Does the video feature a noticeable aerial perspective, where distant scenery appears less detailed, desaturated, and hazier due to atmospheric effects? | 8 | 234 | lighting_setup.natural_effect.aerial_perspective |
| Does the video feature warm, golden sunlight at sunrise or sunset? | 8 | 84 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_sunset_sunrise |
| Does the video feature strong contrasts between highly saturated and desaturated hues? | 8 | 187 | lighting_setup.color_grading.saturation.color_saturation_is_contrasting |
| Is the video predominantly featuring warm colors, such as reds, oranges, or yellows? | 8 | 234 | lighting_setup.color_grading.temperature.color_temperature_is_warm |
| Does the video feature a smooth color shift, with a gradual yet noticeable change in overall or lighting color? | 7 | 235 | lighting_setup.dynamic_light.color_shifting_smooth |
| Is there a silhouette lighting effect that creates a dark outline of the foreground subject against a bright background? | 7 | 235 | lighting_setup.special_effect.silhouette |
| Is the video entirely in black and white, with no color present? | 6 | 236 | lighting_setup.color_grading.is_black_white |
| Does the video feature distinct shadow patterns cast by venetian blinds or similar slatted structures? | 6 | 236 | lighting_setup.shadow_pattern.venetian_blinds |
| Does the video contain anamorphic lens flares as bright, elongated streaks from light interacting with an anamorphic lens? | 6 | 236 | lighting_setup.lens_effect.lens_flares_anamorphic |
| Is there a noticeable light source consistently illuminating the subject from below (bottom lighting) as seen from the camera’s perspective? | 5 | 99 | lighting_setup.subject_lighting.light_direction.direction_is_bottom_light |
| Does the video show noticeable shimmering effects or bright highlights from light reflecting off water? | 5 | 237 | lighting_setup.reflection.reflection_from_water |
| Does the video capture a lightning effect with intense flashes and jagged, branching streaks? | 5 | 237 | lighting_setup.natural_effect.lightning |
| Does the video have noticeable shifts in color saturation between high and low over time? | 5 | 190 | lighting_setup.color_grading.saturation.color_saturation_is_changing |
| Does the video feature visible beams of light with well-defined edges, creating linear volumes of light? | 5 | 237 | lighting_setup.volumetric_lighting.volumetric_beam_light |
| Does the video feature shadows cast by window frames? | 5 | 237 | lighting_setup.shadow_pattern.window_frames |
| Does the video feature water caustics, where light creates dynamic rippling patterns? | 5 | 237 | lighting_setup.special_effect.water_caustics |
| Does the video feature bright and colorful city lighting from various artificial sources? | 5 | 237 | lighting_setup.special_effect.city_light |
| Does the video feature a transformation or morphing effect where one object changes into another? | 4 | 238 | lighting_setup.dynamic_effect.transformation_morphing |
| Does the video show objects breaking, shattering, or fragmenting into smaller pieces? | 3 | 239 | lighting_setup.dynamic_effect.shattering_breaking |
| Does the video show strong reflections from light bouncing off a mirror, clearly mirroring the scenery in detail? | 2 | 240 | lighting_setup.reflection.reflection_from_mirror |
| Is the video showing a scene that is extremely dark and underexposed, with minimal lighting and most areas showing barely any visible details? | 2 | 240 | lighting_setup.color_grading.brightness.brightness_is_very_dark |
| Does the video use a mist diffusion filter to soften the image, creating a dreamy, glowing effect? | 2 | 240 | lighting_setup.lens_effect.mist_diffusion |
| Does the video feature light from street lamps? | 2 | 240 | lighting_setup.special_effect.street_light |
| Is there Rembrandt lighting that illuminates one side of the subject’s face, creating a small triangle of light on the other? | 1 | 241 | lighting_setup.subject_lighting.rembrandt_lighting |
| Does the video feature a noticeable heat haze effect, with air distortions and shimmering caused by rising heat? | 1 | 241 | lighting_setup.natural_effect.heat_haze |
| Does the video feature a noticeable rainbow? | 1 | 241 | lighting_setup.natural_effect.rainbow |
| Is moonlight or starlight a primary light source, with the moon or stars visible? | 1 | 241 | lighting_setup.light_source.has_moonlight_starlight |
| Does the video feature an aurora, with flowing, colorful light patterns in the sky? | 0 | 242 | lighting_setup.natural_effect.aurora |
| Is the video excessively bright and overexposed, making details hard to see? | 0 | 242 | lighting_setup.color_grading.brightness.brightness_is_very_bright |
| Does the video feature a headlight or flashlight that illuminates the scene in front with intense, focused light, creating sharp contrast against darker surroundings? | 0 | 242 | lighting_setup.special_effect.headlight_flashlight |
