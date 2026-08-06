class LightingSetupData:
    def __init__(self):
        # Is labeled?
        self.is_labeled = True  # Boolean: True or False

        # Shot transition options
        self.shot_transition = None # Boolean: True or False

        # Color temperature options
        # Options: "warm", "neutral", "cool", "black_white", "complex_changing", "complex_contrasting", "complex_others"
        self.color_temperature = "complex_others"

        # Colorfulness options
        # Options: "high_colorfulness", "neutral", "low_colorfulness", "black_white", "complex_changing", "complex_contrasting", "complex_others"
        self.colorfulness = "complex_others"

        # Brightness level options
        # Options: "very_bright", "bright_deprecated", "neutral", "dark_deprecated", "very_dark", "complex_changing", "complex_contrasting", "complex_others"
        self.brightness = "complex_others"

        # Color grading description
        self.color_grading_description = ""

        # Scene type options
        # Options: "interior", "exterior", "unrealistic_synthetic", "complex_others"
        self.scene_type = "complex_others"

        # Major light sources
        self.sunlight_source = None
        self.moonlight_starlight_source = None
        self.firelight_source = None
        self.artificial_light_source = None
        self.non_visible_light_source = None
        # self.abstract_light_source = None
        self.unclear_or_changing_light_source = None

        # Sunlight level
        self.sunlight_level = "unknown"  # Options: "normal", "sunny", "overcast", "sunset_sunrise", "unknown"

        # Light quality
        self.light_quality = "complex_ambiguous"  # Options: "hard_light", "soft_light", "complex_changing", "complex_ambiguous"

        # Lighting setup description
        self.lighting_setup_description = ""

        # Subject lighting
        self.subject_condition = "unrealistic"  # Options: "unrealistic", "unclear_subject", "inconsistent_subject", "consistent_subject"

        # Contrast ratio on subject
        self.subject_contrast_ratio = "unknown"  # Options: "high_contrast", "normal_contrast", "minimal_contrast", "complex_changing", "complex_contrasting", "complex_others", "unknown"

        # Direction of major light on subject
        self.subject_light_direction = "unknown"  # Options: "consistent", "complex_changing", "complex_contrasting", "complex_others", "unknown"
        self.subject_back_light = None
        self.subject_front_light = None
        self.subject_top_light = None
        self.subject_bottom_light = None
        self.subject_right_side_light = None
        self.subject_left_side_light = None
        self.subject_ambient_light = None

        # Special lighting effects on subject
        self.rembrandt_lighting = None
        # below two are actually not dependent on whether the subject is present or not
        self.silhouette = None
        self.rim_light = None

        # Subject lighting description
        self.subject_lighting_description = ""

        # Lens and optical effects
        self.lens_flares_regular = None
        self.lens_flares_anamorphic = None
        self.mist_diffusion = None
        self.bokeh = None

        # Reflection lights
        self.reflection_from_water = None
        self.reflection_from_glossy_surface = None
        self.reflection_from_mirror = None

        # Special natural lighting effects
        self.aerial_perspective = None
        self.rainbow = None
        self.aurora = None
        self.heat_haze = None
        self.lightning = None

        # Special lighting effects on the scene
        self.professional_lighting = None
        self.colored_neon_lighting = None
        self.headlight_flashlight = None
        self.vignette = None
        self.water_caustics = None
        self.city_light = None
        self.street_light = None

        # Special lighting effects description
        self.special_lighting_description = ""

        # Volumetric lighting types
        self.volumetric_beam_light = None
        self.volumetric_spot_light = None
        self.god_rays = None
        self.light_through_medium = None
        self.volumetric_light_others = None

        # Volumetric lighting description
        self.volumetric_lighting_description = ""

        # Shadow pattern or Gobo lighting
        self.venetian_blinds = None
        self.subject_shape = None
        self.window_frames = None
        self.foliage = None
        self.shadow_patterns_gobo_others = None

        # Shadow pattern description
        self.shadow_pattern_description = ""

        # Lighting dynamics
        self.color_shifting_smooth = None
        self.color_shifting_sudden = None
        self.pulsing_flickering = None
        self.flashing = None
        self.moving_light = None

        # Lighting dynamics description
        self.lighting_dynamics_description = ""

        # Dynamic effects
        self.revealing_shot = None
        self.transformation_morphing = None
        self.levitation_floating = None
        self.explosion = None
        self.shattering_breaking = None
        self.diffusion = None
        self.splashing_waves = None

    def set_lighting_setup_attributes(self):
        self._set_color_grading_attributes()
        self._set_lighting_setup_attributes()
        self._set_subject_lighting_attributes()
        self._set_special_lighting_attributes()
        self._set_volumetric_lighting_attributes()
        self._set_shadow_pattern_attributes()

    def _set_color_grading_attributes(self):
        attributes = [
            "is_color_grading_complex", "is_black_white",
            # "is_brighter_than_normal", "is_darker_than_normal",
            "color_temperature_is_warm", "color_temperature_is_cool", "color_temperature_is_neutral",
            "color_temperature_is_complex_changing", "color_temperature_is_complex_contrasting",
            "color_temperature_is_complex_others",
            "colorfulness_is_high", "colorfulness_is_low", "colorfulness_is_neutral",
            "colorfulness_is_complex_changing", "colorfulness_is_complex_contrasting",
            "colorfulness_is_complex_others",
            "brightness_is_very_bright", 
            # "brightness_is_bright", 
            "brightness_is_neutral",
            # "brightness_is_dark", 
            "brightness_is_very_dark",
            "brightness_is_complex_changing", "brightness_is_complex_contrasting",
            "brightness_is_complex_others"
        ]

        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return

        complex_types = {"complex_changing", "complex_contrasting", "complex_others"}

        # Complex color grading check
        self.is_color_grading_complex = any([
            self.color_temperature in complex_types,
            self.colorfulness in complex_types,
            self.brightness in complex_types
        ])

        # Black & white check
        self.is_black_white = (
            self.colorfulness == "black_white" or 
            self.color_temperature == "black_white"
        )

        # Color temperature attributes
        self.color_temperature_is_warm = self.color_temperature == "warm"
        self.color_temperature_is_cool = self.color_temperature == "cool"
        self.color_temperature_is_neutral = self.color_temperature == "neutral"

        if self.color_temperature != "complex_others":
            self.color_temperature_is_complex_changing = self.color_temperature == "complex_changing"
            self.color_temperature_is_complex_contrasting = self.color_temperature == "complex_contrasting"
        else:
            self.color_temperature_is_complex_changing = True
            self.color_temperature_is_complex_contrasting = True

        self.color_temperature_is_complex_others = self.color_temperature == "complex_others"

        # Colorfulness attributes
        self.colorfulness_is_high = self.colorfulness == "high_colorfulness"
        self.colorfulness_is_low = self.colorfulness == "low_colorfulness"
        self.colorfulness_is_neutral = self.colorfulness == "neutral"

        if self.colorfulness != "complex_others":
            self.colorfulness_is_complex_changing = self.colorfulness == "complex_changing"
            self.colorfulness_is_complex_contrasting = self.colorfulness == "complex_contrasting"
        else:
            self.colorfulness_is_complex_changing = True
            self.colorfulness_is_complex_contrasting = True

        self.colorfulness_is_complex_others = self.colorfulness == "complex_others"

        # Brightness attributes
        # self.is_brighter_than_normal = self.brightness in {"very_bright", "bright"}
        # self.is_darker_than_normal = self.brightness in {"dark", "very_dark"}

        self.brightness_is_very_bright = self.brightness == "very_bright"
        # self.brightness_is_bright = self.brightness == "bright"
        self.brightness_is_neutral = self.brightness == "neutral"
        # self.brightness_is_dark = self.brightness == "dark"
        self.brightness_is_very_dark = self.brightness == "very_dark"

        if self.brightness != "complex_others":
            self.brightness_is_complex_changing = self.brightness == "complex_changing"
            self.brightness_is_complex_contrasting = self.brightness == "complex_contrasting"
        else:
            self.brightness_is_complex_changing = True
            self.brightness_is_complex_contrasting = True

        self.brightness_is_complex_others = self.brightness == "complex_others"

    def _set_lighting_setup_attributes(self):
        attributes = [
            # "is_lighting_quality_complex",
            "scene_type_is_unclear_or_changing", "scene_type_is_exterior",
            "scene_type_is_interior", "scene_type_is_synthetic",
            "sunlight_quality_is_normal", "sunlight_quality_is_hard",
            "sunlight_quality_is_soft", "sunlight_quality_is_sunset_sunrise",
            "sunlight_quality_is_unknown",
            "light_quality_is_soft",
            "light_quality_is_hard", "light_quality_is_changing",
            "light_quality_is_complex_ambiguous"
        ]
        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return
        # self.is_lighting_quality_complex = self.light_quality in {"complex_changing", "complex_contrasting", "complex_others"}
        self.scene_type_is_unclear_or_changing = self.scene_type == "complex_others"
        self.scene_type_is_exterior = self.scene_type == "exterior" if not self.scene_type in ["complex_others", "unrealistic_synthetic"] else None
        self.scene_type_is_interior = self.scene_type == "interior" if not self.scene_type in ["complex_others", "unrealistic_synthetic"] else None
        self.scene_type_is_synthetic = self.scene_type == "unrealistic_synthetic"

        if self.sunlight_level == "unknown":
            self.sunlight_quality_is_normal = None
            self.sunlight_quality_is_hard = None
            self.sunlight_quality_is_soft = None
            self.sunlight_quality_is_sunset_sunrise = None
        else:
            self.sunlight_quality_is_normal = self.sunlight_level == "normal"
            self.sunlight_quality_is_hard = self.sunlight_level == "sunny"
            self.sunlight_quality_is_soft = self.sunlight_level == "overcast"
            self.sunlight_quality_is_sunset_sunrise = self.sunlight_level == "sunset_sunrise"

        self.sunlight_quality_is_unknown = self.sunlight_level == "unknown"

        # Light Quality
        self.light_quality_is_complex_ambiguous = self.light_quality == "complex_ambiguous"
        if not self.light_quality_is_complex_ambiguous:
            self.light_quality_is_soft = self.light_quality == "soft_light"
            self.light_quality_is_hard = self.light_quality == "hard_light"
            self.light_quality_is_changing = self.light_quality == "complex_changing"
        else:
            self.light_quality_is_soft = None
            self.light_quality_is_hard = None
            self.light_quality_is_changing = None

    def _set_subject_lighting_attributes(self):
        attributes = [
            "is_subject_lighting_unrealistic", "is_unclear_or_light_emitting_subject", "is_consistent_subject", "is_inconsistent_subject",
            "subject_light_contrast_is_high", "subject_light_contrast_is_normal", "subject_light_contrast_is_minimal",
            "subject_light_contrast_is_complex_changing", "subject_light_contrast_is_complex_contrasting", "subject_light_contrast_is_complex_others", "subject_light_contrast_is_unknown",
            "flat_lighting", "low_key_lighting", "high_key_lighting", 
            "direction_is_back_light", "direction_is_front_light",
            "direction_is_top_light", "direction_is_bottom_light", "direction_is_right_side", "direction_is_left_side",
            "direction_is_ambient_light", "direction_is_complex_changing", "direction_is_complex_contrasting", "direction_is_complex_others", "direction_is_unknown", "direction_is_consistent"
        ]
        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return
        self.is_subject_lighting_unrealistic = self.subject_condition == "unrealistic"
        self.is_unclear_or_light_emitting_subject = self.subject_condition == "unclear_subject"
        self.is_consistent_subject = self.subject_condition == "consistent_subject"
        self.is_inconsistent_subject = self.subject_condition == "inconsistent_subject"

        # Subject contrast logic
        contrast = self.subject_contrast_ratio
        self.subject_light_contrast_is_unknown = contrast == "unknown"
        if not self.subject_light_contrast_is_unknown:
            self.subject_light_contrast_is_high = contrast == "high_contrast"
            self.subject_light_contrast_is_normal = contrast == "normal_contrast"
            self.subject_light_contrast_is_minimal = contrast == "minimal_contrast"
            self.subject_light_contrast_is_complex_changing = contrast == "complex_changing"
            self.subject_light_contrast_is_complex_contrasting = contrast == "complex_contrasting"
            self.subject_light_contrast_is_complex_others = contrast == "complex_others"
            if self.subject_light_contrast_is_complex_others:
                self.subject_light_contrast_is_complex_changing = True
                self.subject_light_contrast_is_complex_contrasting = True
            self.flat_lighting = self.subject_light_contrast_is_minimal
            self.low_key_lighting = self.subject_light_contrast_is_high is True and self.brightness_is_very_bright is False
            self.high_key_lighting = self.subject_light_contrast_is_minimal is True and self.brightness_is_very_dark is False
        else:
            self.subject_light_contrast_is_high = None
            self.subject_light_contrast_is_normal = None
            self.subject_light_contrast_is_minimal = None
            self.subject_light_contrast_is_complex_changing = None
            self.subject_light_contrast_is_complex_contrasting = None
            self.subject_light_contrast_is_complex_others = None
            self.flat_lighting = None
            self.low_key_lighting = None
            self.high_key_lighting = None

        direction = self.subject_light_direction
        self.direction_is_unknown = direction == "unknown"
        if not self.direction_is_unknown:
            self.direction_is_consistent = direction == "consistent"
            self.direction_is_complex_others = direction == "complex_others"
            self.direction_is_complex_changing = direction == "complex_changing" or direction == "complex_others"
            self.direction_is_complex_contrasting = direction == "complex_contrasting" or direction == "complex_others"
            if self.direction_is_consistent:
                self.direction_is_back_light = self.subject_back_light
                self.direction_is_front_light = self.subject_front_light
                self.direction_is_top_light = self.subject_top_light
                self.direction_is_bottom_light = self.subject_bottom_light
                self.direction_is_right_side = self.subject_right_side_light
                self.direction_is_left_side = self.subject_left_side_light
                self.direction_is_ambient_light = self.subject_ambient_light
            else:
                self.direction_is_back_light = None
                self.direction_is_front_light = None
                self.direction_is_top_light = None
                self.direction_is_bottom_light = None
                self.direction_is_right_side = None
                self.direction_is_left_side = None
                self.direction_is_ambient_light = None
        else:
            self.direction_is_consistent = None
            self.direction_is_complex_others = None
            self.direction_is_complex_changing = None
            self.direction_is_complex_contrasting = None
            self.direction_is_back_light = None
            self.direction_is_front_light = None
            self.direction_is_top_light = None
            self.direction_is_bottom_light = None
            self.direction_is_right_side = None
            self.direction_is_left_side = None
            self.direction_is_ambient_light = None

    def _set_special_lighting_attributes(self):
        if self.shot_transition is True or self.is_labeled is False:
            self.lens_flares = None
            return
        self.lens_flares = self.lens_flares_regular or self.lens_flares_anamorphic

    def _set_volumetric_lighting_attributes(self):
        if self.shot_transition is True or self.is_labeled is False:
            self.has_volumetric_lighting = None
            return
        self.has_volumetric_lighting = self.volumetric_beam_light or self.volumetric_spot_light or self.god_rays or self.light_through_medium or self.volumetric_light_others

    def _set_shadow_pattern_attributes(self):
        if self.shot_transition is True or self.is_labeled is False:
            self.has_shadow_patterns = None
            return
        self.has_shadow_patterns = self.venetian_blinds or self.subject_shape or self.window_frames or self.foliage or self.shadow_patterns_gobo_others

    def set_is_labeled(self, is_labeled):
        if isinstance(is_labeled, bool):
            self.is_labeled = is_labeled
        else:
            raise ValueError("is_labeled must be a boolean value")

    def set_shot_transition(self, shot_transition):
        if isinstance(shot_transition, bool):
            self.shot_transition = shot_transition
        else:
            raise ValueError("shot_transition must be a boolean value")

    def set_color_temperature(self, color_temperature):
        if color_temperature in ["warm", "neutral", "cool", "black_white", "complex_changing", "complex_contrasting", "complex_others"]:
            self.color_temperature = color_temperature
        else:
            raise ValueError("color_temperature must be one of 'warm', 'neutral', 'cool', 'black_white', 'complex_changing', 'complex_contrasting', 'complex_others'")

    def set_colorfulness(self, colorfulness):
        if colorfulness in ["high_colorfulness", "neutral", "low_colorfulness", "black_white", "complex_changing", "complex_contrasting", "complex_others"]:
            self.colorfulness = colorfulness
        else:
            raise ValueError("colorfulness must be one of 'high_colorfulness', 'neutral', 'low_colorfulness', 'black_white', 'complex_changing', 'complex_contrasting', 'complex_others'")

    def set_brightness(self, brightness):
        if brightness in ["very_bright", "bright", "neutral", "dark", "very_dark", "complex_changing", "complex_contrasting", "complex_others"]:
            self.brightness = brightness
        else:
            raise ValueError("brightness must be one of 'very_bright', 'bright', 'neutral', 'dark', 'very_dark', 'complex_changing', 'complex_contrasting', 'complex_others'")

    def set_scene_type(self, scene_type):
        if scene_type in ["interior", "exterior", "unrealistic_synthetic", "complex_others"]:
            self.scene_type = scene_type
        else:
            raise ValueError("scene_type must be one of 'interior', 'exterior', 'unrealistic_synthetic', 'complex_others'")

    def set_sunlight_level(self, sunlight_level):
        if sunlight_level in ["normal", "sunny", "overcast", "sunset_sunrise", "unknown"]:
            self.sunlight_level = sunlight_level
        else:
            raise ValueError("sunlight_level must be one of 'normal', 'sunny', 'overcast', 'sunset_sunrise', 'unknown'")

    def set_light_quality(self, light_quality):
        if light_quality in ["hard_light", "soft_light", "complex_changing", "complex_ambiguous"]:
            self.light_quality = light_quality
        else:
            raise ValueError("light_quality must be one of 'hard_light', 'soft_light', 'complex_changing', 'complex_ambiguous'")

    def set_subject_contrast_ratio(self, subject_contrast_ratio):
        if subject_contrast_ratio in ["high_contrast", "normal_contrast", "minimal_contrast", "complex_changing", "complex_contrasting", "complex_others", "unknown"]:
            self.subject_contrast_ratio = subject_contrast_ratio
        else:
            raise ValueError("subject_contrast_ratio must be one of 'high_contrast', 'normal_contrast', 'minimal_contrast', 'complex_changing', 'complex_contrasting', 'complex_others', 'unknown'")

    def set_sunlight_source(self, sunlight_source):
        if isinstance(sunlight_source, bool):
            self.sunlight_source = sunlight_source
        else:
            raise ValueError("sunlight_source must be a boolean value")

    def set_moonlight_starlight_source(self, moonlight_starlight_source):
        if isinstance(moonlight_starlight_source, bool):
            self.moonlight_starlight_source = moonlight_starlight_source
        else:
            raise ValueError("moonlight_starlight_source must be a boolean value")

    def set_firelight_source(self, firelight_source):
        if isinstance(firelight_source, bool):
            self.firelight_source = firelight_source
        else:
            raise ValueError("firelight_source must be a boolean value")

    def set_artificial_light_source(self, artificial_light_source):
        if isinstance(artificial_light_source, bool):
            self.artificial_light_source = artificial_light_source
        else:
            raise ValueError("artificial_light_source must be a boolean value")

    def set_non_visible_light_source(self, non_visible_light_source):
        if isinstance(non_visible_light_source, bool):
            self.non_visible_light_source = non_visible_light_source
        else:
            raise ValueError("non_visible_light_source must be a boolean value")

    # def set_abstract_light_source(self, abstract_light_source):
    #     if isinstance(abstract_light_source, bool):
    #         self.abstract_light_source = abstract_light_source
    #     else:
    #         raise ValueError("abstract_light_source must be a boolean value")

    def set_unclear_or_changing_light_source(self, unclear_or_changing_light_source):
        if isinstance(unclear_or_changing_light_source, bool):
            self.unclear_or_changing_light_source = unclear_or_changing_light_source
        else:
            raise ValueError("unclear_or_changing_light_source must be a boolean value")

    def set_subject_back_light(self, subject_back_light):
        if isinstance(subject_back_light, bool):
            self.subject_back_light = subject_back_light
        else:
            raise ValueError("subject_back_light must be a boolean value")

    def set_subject_front_light(self, subject_front_light):
        if isinstance(subject_front_light, bool):
            self.subject_front_light = subject_front_light
        else:
            raise ValueError("subject_front_light must be a boolean value")

    def set_subject_top_light(self, subject_top_light):
        if isinstance(subject_top_light, bool):
            self.subject_top_light = subject_top_light
        else:
            raise ValueError("subject_top_light must be a boolean value")

    def set_subject_bottom_light(self, subject_bottom_light):
        if isinstance(subject_bottom_light, bool):
            self.subject_bottom_light = subject_bottom_light
        else:
            raise ValueError("subject_bottom_light must be a boolean value")

    def set_subject_ambient_light(self, subject_ambient_light):
        if isinstance(subject_ambient_light, bool):
            self.subject_ambient_light = subject_ambient_light
        else:
            raise ValueError("subject_ambient_light must be a boolean value")

    def set_professional_lighting(self, professional_lighting):
        if isinstance(professional_lighting, bool):
            self.professional_lighting = professional_lighting
        else:
            raise ValueError("professional_lighting must be a boolean value")

    def set_rembrandt_lighting(self, rembrandt_lighting):
        if isinstance(rembrandt_lighting, bool):
            self.rembrandt_lighting = rembrandt_lighting
        else:
            raise ValueError("rembrandt_lighting must be a boolean value")

    def set_silhouette(self, silhouette):
        if isinstance(silhouette, bool):
            self.silhouette = silhouette
        else:
            raise ValueError("silhouette must be a boolean value")

    def set_rim_light(self, rim_light):
        if isinstance(rim_light, bool):
            self.rim_light = rim_light
        else:
            raise ValueError("rim_light must be a boolean value")

    def set_lens_flares_regular(self, lens_flares_regular):
        if isinstance(lens_flares_regular, bool):
            self.lens_flares_regular = lens_flares_regular
        else:
            raise ValueError("lens_flares_regular must be a boolean value")

    def set_lens_flares_anamorphic(self, lens_flares_anamorphic):
        if isinstance(lens_flares_anamorphic, bool):
            self.lens_flares_anamorphic = lens_flares_anamorphic
        else:
            raise ValueError("lens_flares_anamorphic must be a boolean value")

    def set_mist_diffusion(self, mist_diffusion):
        if isinstance(mist_diffusion, bool):
            self.mist_diffusion = mist_diffusion
        else:
            raise ValueError("mist_diffusion must be a boolean value")

    def set_bokeh(self, bokeh):
        if isinstance(bokeh, bool):
            self.bokeh = bokeh
        else:
            raise ValueError("bokeh must be a boolean value")

    def set_reflection_from_water(self, reflection_from_water):
        if isinstance(reflection_from_water, bool):
            self.reflection_from_water = reflection_from_water
        else:
            raise ValueError("reflection_from_water must be a boolean value")

    def set_reflection_from_glossy_surface(self, reflection_from_glossy_surface):
        if isinstance(reflection_from_glossy_surface, bool):
            self.reflection_from_glossy_surface = reflection_from_glossy_surface
        else:
            raise ValueError("reflection_from_glossy_surface must be a boolean value")

    def set_reflection_from_mirror(self, reflection_from_mirror):
        if isinstance(reflection_from_mirror, bool):
            self.reflection_from_mirror = reflection_from_mirror
        else:
            raise ValueError("reflection_from_mirror must be a boolean value")

    def set_rainbow(self, rainbow):
        if isinstance(rainbow, bool):
            self.rainbow = rainbow
        else:
            raise ValueError("rainbow must be a boolean value")

    def set_heat_haze(self, heat_haze):
        if isinstance(heat_haze, bool):
            self.heat_haze = heat_haze
        else:
            raise ValueError("heat_haze must be a boolean value")

    def set_aurora(self, aurora):
        if isinstance(aurora, bool):
            self.aurora = aurora
        else:
            raise ValueError("aurora must be a boolean value")

    def set_aerial_perspective(self, aerial_perspective):
        if isinstance(aerial_perspective, bool):
            self.aerial_perspective = aerial_perspective
        else:
            raise ValueError("aerial_perspective must be a boolean value")

    def set_lightning(self, lightning):
        if isinstance(lightning, bool):
            self.lightning = lightning
        else:
            raise ValueError("lightning must be a boolean value")

    def set_colored_neon_lighting(self, colored_neon_lighting):
        if isinstance(colored_neon_lighting, bool):
            self.colored_neon_lighting = colored_neon_lighting
        else:
            raise ValueError("colored_neon_lighting must be a boolean value")

    def set_headlight_flashlight(self, headlight_flashlight):
        if isinstance(headlight_flashlight, bool):
            self.headlight_flashlight = headlight_flashlight
        else:
            raise ValueError("headlight_flashlight must be a boolean value")

    def set_vignette(self, vignette):
        if isinstance(vignette, bool):
            self.vignette = vignette
        else:
            raise ValueError("vignette must be a boolean value")

    def set_water_caustics(self, water_caustics):
        if isinstance(water_caustics, bool):
            self.water_caustics = water_caustics
        else:
            raise ValueError("water_caustics must be a boolean value")

    def set_city_light(self, city_light):
        if isinstance(city_light, bool):
            self.city_light = city_light
        else:
            raise ValueError("city_light must be a boolean value")

    def set_street_light(self, street_light):
        if isinstance(street_light, bool):
            self.street_light = street_light
        else:
            raise ValueError("street_light must be a boolean value")

    def set_volumetric_beam_light(self, volumetric_beam_light):
        if isinstance(volumetric_beam_light, bool):
            self.volumetric_beam_light = volumetric_beam_light
        else:
            raise ValueError("volumetric_beam_light must be a boolean value")

    def set_volumetric_spot_light(self, volumetric_spot_light):
        if isinstance(volumetric_spot_light, bool):
            self.volumetric_spot_light = volumetric_spot_light
        else:
            raise ValueError("volumetric_spot_light must be a boolean value")

    def set_god_rays(self, god_rays):
        if isinstance(god_rays, bool):
            self.god_rays = god_rays
        else:
            raise ValueError("god_rays must be a boolean value")

    def set_light_through_medium(self, light_through_medium):
        if isinstance(light_through_medium, bool):
            self.light_through_medium = light_through_medium
        else:
            raise ValueError("light_through_medium must be a boolean value")

    def set_volumetric_light_others(self, volumetric_light_others):
        if isinstance(volumetric_light_others, bool):
            self.volumetric_light_others = volumetric_light_others
        else:
            raise ValueError("volumetric_light_others must be a boolean value")

    def set_venetian_blinds(self, venetian_blinds):
        if isinstance(venetian_blinds, bool):
            self.venetian_blinds = venetian_blinds
        else:
            raise ValueError("venetian_blinds must be a boolean value")

    def set_subject_shape(self, subject_shape):
        if isinstance(subject_shape, bool):
            self.subject_shape = subject_shape
        else:
            raise ValueError("subject_shape must be a boolean value")

    def set_window_frames(self, window_frames):
        if isinstance(window_frames, bool):
            self.window_frames = window_frames
        else:
            raise ValueError("window_frames must be a boolean value")

    def set_foliage(self, foliage):
        if isinstance(foliage, bool):
            self.foliage = foliage
        else:
            raise ValueError("foliage must be a boolean value")

    def set_shadow_patterns_gobo_others(self, shadow_patterns_gobo_others):
        if isinstance(shadow_patterns_gobo_others, bool):
            self.shadow_patterns_gobo_others = shadow_patterns_gobo_others
        else:
            raise ValueError("shadow_patterns_gobo_others must be a boolean value")

    def set_color_shifting_smooth(self, color_shifting_smooth):
        if isinstance(color_shifting_smooth, bool):
            self.color_shifting_smooth = color_shifting_smooth
        else:
            raise ValueError("color_shifting_smooth must be a boolean value")

    def set_color_shifting_sudden(self, color_shifting_sudden):
        if isinstance(color_shifting_sudden, bool):
            self.color_shifting_sudden = color_shifting_sudden
        else:
            raise ValueError("color_shifting_sudden must be a boolean value")

    def set_pulsing_flickering(self, pulsing_flickering):
        if isinstance(pulsing_flickering, bool):
            self.pulsing_flickering = pulsing_flickering
        else:
            raise ValueError("pulsing_flickering must be a boolean value")

    def set_flashing(self, flashing):
        if isinstance(flashing, bool):
            self.flashing = flashing
        else:
            raise ValueError("flashing must be a boolean value")

    def set_moving_light(self, moving_light):
        if isinstance(moving_light, bool):
            self.moving_light = moving_light
        else:
            raise ValueError("moving_light must be a boolean value")

    def set_revealing_shot(self, revealing_shot):
        if isinstance(revealing_shot, bool):
            self.revealing_shot = revealing_shot
        else:
            raise ValueError("revealing_shot must be a boolean value")

    def set_transformation_morphing(self, transformation_morphing):
        if isinstance(transformation_morphing, bool):
            self.transformation_morphing = transformation_morphing
        else:
            raise ValueError("transformation_morphing must be a boolean value")

    def set_levitation_floating(self, levitation_floating):
        if isinstance(levitation_floating, bool):
            self.levitation_floating = levitation_floating
        else:
            raise ValueError("levitation_floating must be a boolean value")

    def set_explosion(self, explosion):
        if isinstance(explosion, bool):
            self.explosion = explosion
        else:
            raise ValueError("explosion must be a boolean value")

    def set_shattering_breaking(self, shattering_breaking):
        if isinstance(shattering_breaking, bool):
            self.shattering_breaking = shattering_breaking
        else:
            raise ValueError("shattering_breaking must be a boolean value")

    def set_diffusion(self, diffusion):
        if isinstance(diffusion, bool):
            self.diffusion = diffusion
        else:
            raise ValueError("diffusion must be a boolean value")

    def set_splashing_waves(self, splashing_waves):
        if isinstance(splashing_waves, bool):
            self.splashing_waves = splashing_waves
        else:
            raise ValueError("splashing_waves must be a boolean value")

    def set_color_grading_description(self, color_grading_description):
        if isinstance(color_grading_description, str):
            self.color_grading_description = color_grading_description
        else:
            raise ValueError("color_grading_description must be a string value")

    def set_lighting_setup_description(self, lighting_setup_description):
        if isinstance(lighting_setup_description, str):
            self.lighting_setup_description = lighting_setup_description
        else:
            raise ValueError("lighting_setup_description must be a string value")

    def set_subject_lighting_description(self, subject_lighting_description):
        if isinstance(subject_lighting_description, str):
            self.subject_lighting_description = subject_lighting_description
        else:
            raise ValueError("subject_lighting_description must be a string value")

    def set_special_lighting_description(self, special_lighting_description):
        if isinstance(special_lighting_description, str):
            self.special_lighting_description = special_lighting_description
        else:
            raise ValueError("special_lighting_description must be a string value")

    def set_volumetric_lighting_description(self, volumetric_lighting_description):
        if isinstance(volumetric_lighting_description, str):
            self.volumetric_lighting_description = volumetric_lighting_description
        else:
            raise ValueError("volumetric_lighting_description must be a string value")

    def set_shadow_pattern_description(self, shadow_pattern_description):
        if isinstance(shadow_pattern_description, str):
            self.shadow_pattern_description = shadow_pattern_description
        else:
            raise ValueError("shadow_pattern_description must be a string value")

    def set_lighting_dynamics_description(self, lighting_dynamics_description):
        if isinstance(lighting_dynamics_description, str):
            self.lighting_dynamics_description = lighting_dynamics_description
        else:
            raise ValueError("lighting_dynamics_description must be a string value")

    def set_subject_condition(self, subject_condition):
        if subject_condition in ["unrealistic", "unclear_subject", "inconsistent_subject", "consistent_subject"]:
            self.subject_condition = subject_condition
        else:
            raise ValueError("subject_condition must be one of 'unrealistic', 'unclear_subject', 'inconsistent_subject', 'consistent_subject'")

    def set_subject_light_direction(self, subject_light_direction):
        if subject_light_direction in ["consistent", "complex_changing", "complex_contrasting", "complex_others", "unknown"]:
            self.subject_light_direction = subject_light_direction
        else:
            raise ValueError("subject_light_direction must be one of 'consistent', 'complex_changing', 'complex_contrasting', 'complex_others', 'unknown'")

    def set_subject_right_side_light(self, subject_right_side_light):
        if isinstance(subject_right_side_light, bool):
            self.subject_right_side_light = subject_right_side_light
        else:
            raise ValueError("subject_right_side_light must be a boolean value")

    def set_subject_left_side_light(self, subject_left_side_light):
        if isinstance(subject_left_side_light, bool):
            self.subject_left_side_light = subject_left_side_light
        else:
            raise ValueError("subject_left_side_light must be a boolean value")

    @classmethod
    def create(cls, **kwargs):
        """Create a LightingSetupData instance ensuring all attributes are set using setters."""
        instance = cls()
        for key, value in kwargs.items():
            setter_method = getattr(instance, f"set_{key}", None)
            if setter_method and callable(setter_method):
                setter_method(value)
            else:
                raise AttributeError(f"Invalid attribute: {key} or setter method not found")
        instance.verify()
        instance.set_lighting_setup_attributes()
        return instance

    def update(self, **kwargs):
        """Update the attributes of the LightingSetupData instance."""
        for key, value in kwargs.items():
            setter_method = getattr(self, f"set_{key}", None)
            if setter_method and callable(setter_method):
                setter_method(value)
            else:
                raise AttributeError(f"Invalid attribute: {key} or setter method not found")
        self.verify()
        self.set_lighting_setup_attributes()

    def verify(self):
        # Verify that the data is consistent
        if self.shot_transition is True or self.is_labeled is False:
            return # No need to verify other fields if shot transition is present or data is not labeled

        # Verify subject condition rules
        if self.subject_condition == "unclear_subject":
            if self.subject_light_direction != "unknown":
                raise ValueError("subject_light_direction must be 'unknown' when subject_condition is 'unclear_subject'")
            if self.subject_contrast_ratio != "unknown":
                raise ValueError("subject_contrast_ratio must be 'unknown' when subject_condition is 'unclear_subject'")
            
            if any([self.subject_back_light, self.subject_front_light, self.subject_top_light, 
                    self.subject_bottom_light, self.subject_right_side_light, self.subject_left_side_light, 
                    self.subject_ambient_light]):
                raise ValueError("All light direction attributes must be False when subject_condition is 'unclear_subject'")
        
        elif self.subject_condition == "unrealistic":
            if self.subject_light_direction != "unknown":
                raise ValueError("subject_light_direction must be 'unknown' when subject_condition is 'unrealistic'")
            if self.subject_contrast_ratio != "unknown":
                raise ValueError("subject_contrast_ratio must be 'unknown' when subject_condition is 'unrealistic'")
        
        elif self.subject_condition == "inconsistent_subject":
            complex_types = ["complex_changing", "complex_contrasting", "complex_others"]
            if self.subject_contrast_ratio in complex_types:
                raise ValueError("subject_contrast_ratio cannot be complex when subject_condition is 'inconsistent_subject'")
            if self.subject_light_direction in complex_types:
                raise ValueError("subject_light_direction cannot be complex when subject_condition is 'inconsistent_subject'")
        
        elif self.subject_condition == "consistent_subject":
            if self.subject_contrast_ratio == "unknown":
                raise ValueError("subject_contrast_ratio cannot be 'unknown' when subject_condition is 'consistent_subject'")
            if self.subject_light_direction == "unknown":
                raise ValueError("subject_light_direction cannot be 'unknown' when subject_condition is 'consistent_subject'")

        # Verify complex_others logic
        complex_types = ["complex_changing", "complex_contrasting", "complex_others", "unknown"]
        if self.subject_light_direction in complex_types:
            if any([self.subject_back_light, self.subject_front_light, self.subject_top_light, 
                    self.subject_bottom_light, self.subject_right_side_light, self.subject_left_side_light, 
                    self.subject_ambient_light]):
                raise ValueError("All light direction attributes must be False when subject_light_direction is complex or unknown")

        # If ambient light is True, then all other light direction attributes must be False
        if self.subject_ambient_light:
            if any([self.subject_back_light, self.subject_front_light, self.subject_top_light, 
                    self.subject_bottom_light, self.subject_right_side_light, self.subject_left_side_light]):
                raise ValueError("All light direction attributes must be False when subject_ambient_light is True")

        # Verify side light exclusivity
        if self.subject_right_side_light and self.subject_left_side_light:
            raise ValueError("Cannot have both right and left side light")

        # Rest of the verification logic...
        if self.color_temperature == "black_white":
            if not self.colorfulness == "black_white":
                raise ValueError("colorfulness must be 'black_white' if color_temperature is 'black_white'")

        # Make sure brightness is not deprecated
        if self.brightness == "bright_deprecated" or self.brightness == "dark_deprecated":
            raise ValueError("brightness cannot be 'bright_deprecated' or 'dark_deprecated'")

        # if self.abstract_light_source:
        #     if any([self.sunlight_source, self.moonlight_starlight_source, self.firelight_source, self.artificial_light_source, self.non_visible_light_source, self.unclear_or_changing_light_source]):
        #         raise ValueError("abstract_light_source cannot be combined with other light sources")

        #     # scene type must be "unrealistic_synthetic"
        #     if self.scene_type != "unrealistic_synthetic":
        #         raise ValueError("scene_type must be 'unrealistic_synthetic' if abstract_light_source is True")
        
        if self.scene_type == "unrealistic_synthetic":
            if any([self.sunlight_source, self.moonlight_starlight_source, self.firelight_source, self.artificial_light_source, self.non_visible_light_source, self.unclear_or_changing_light_source]):
                raise ValueError("No other light sources can be present if scene_type is 'unrealistic_synthetic'")
            
            # if not self.abstract_light_source:
            #     raise ValueError("abstract_light_source must be True if scene_type is 'unrealistic_synthetic'")

        # if self.sunlight_source:
        #     if self.sunlight_level == "unknown":
        #         raise ValueError("sunlight_level must be specified for sunlight source")
        # else:
        if self.sunlight_level != "unknown" and self.sunlight_source is False:
            raise ValueError("sunlight_level must be 'unknown' if sunlight source is not present")

        # if self.subject_contrast_ratio == "unknown":
        #     if any([self.subject_back_light, self.subject_front_light, self.subject_top_light, self.subject_bottom_light, self.subject_right_side_light, \
        #         self.subject_left_side_light, self.subject_ambient_light, self.rembrandt_lighting]):
        #         raise ValueError("subject_contrast_ratio must be specified if subject lighting is present")

        # Additional check for revealing_shot
        if self.revealing_shot is True and self.subject_condition == "consistent_subject":
            raise ValueError("subject_condition cannot be 'consistent_subject' when revealing_shot is True")


lighting_setup_params_demo = {
    "shot_transition": False,
    "color_temperature": "cool",
    "colorfulness": "high_colorfulness",
    "brightness": "very_bright",
    "color_grading_description": "Cool tones with high saturation and bright lighting",
    "scene_type": "interior",
    "sunlight_source": True,
    "moonlight_starlight_source": False,
    "firelight_source": False,
    "artificial_light_source": False,
    "non_visible_light_source": False,
    # "abstract_light_source": False,
    "unclear_or_changing_light_source": False,
    "sunlight_level": "sunny",
    "light_quality": "soft_light",
    "lighting_setup_description": "Soft diffused light with sunny outdoor setting",
    "subject_condition": "consistent_subject",
    "subject_contrast_ratio": "high_contrast",
    "subject_light_direction": "consistent",
    "subject_back_light": True,
    "subject_front_light": False,
    "subject_top_light": False,
    "subject_bottom_light": False,
    "subject_right_side_light": False,
    "subject_left_side_light": False,
    "subject_ambient_light": False,
    "professional_lighting": True,
    "rembrandt_lighting": False,
    "silhouette": False,
    "rim_light": False,
    "subject_lighting_description": "Portrait lighting with high contrast",
    "lens_flares_regular": False,
    "lens_flares_anamorphic": False,
    "mist_diffusion": False,
    "bokeh": False,
    "reflection_from_water": False,
    "reflection_from_glossy_surface": False,
    "reflection_from_mirror": False,
    "rainbow": False,
    "heat_haze": False,
    "aurora": False,
    "aerial_perspective": False,
    "lightning": False,
    "colored_neon_lighting": False,
    "headlight_flashlight": False,
    "vignette": False,
    "water_caustics": False,
    "city_light": False,
    "street_light": False,
    "special_lighting_description": "Portrait lighting with high contrast",
    "volumetric_beam_light": True,
    "volumetric_spot_light": False,
    "god_rays": False,
    "light_through_medium": False,
    "volumetric_light_others": False,
    "volumetric_lighting_description": "Volumetric beam light effects",
    "venetian_blinds": False,
    "subject_shape": False,
    "window_frames": False,
    "foliage": False,
    "shadow_patterns_gobo_others": False,
    "shadow_pattern_description": "",
    "color_shifting_smooth": True,
    "color_shifting_sudden": False,
    "pulsing_flickering": True,
    "flashing": False,
    "moving_light": False,
    "lighting_dynamics_description": "Smooth color shifting and pulsing effects",
    "revealing_shot": False,
    "transformation_morphing": False,
    "levitation_floating": False,
    "explosion": False,
    "shattering_breaking": False,
    "diffusion": True,
    "splashing_waves": False
}
def create_lighting_setup_data_demo():
    data = LightingSetupData.create(**lighting_setup_params_demo)
    return data

if __name__ == "__main__":
    create_lighting_setup_data_demo()
