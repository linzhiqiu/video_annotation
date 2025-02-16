class LightingSetupData:
    def __init__(self):
        # Shot transition options
        self.shot_transition = False # Boolean: True or False
        
        # Color temperature options
        # Options: "warm", "neutral", "cool", "black_white", "complex_changing", "complex_contrasting", "complex_others"
        self.color_temperature = "neutral"
        
        # Color saturation options
        # Options: "high_saturation", "neutral", "low_saturation", "black_white", "complex_changing", "complex_contrasting", "complex_others"
        self.color_saturation = "neutral"
        
        # Brightness level options
        # Options: "very_bright", "bright", "neutral", "dark", "very_dark", "complex_changing", "complex_contrasting", "complex_others"
        self.brightness = "neutral"
        
        # Color grading description
        self.color_grading_description = ""
        
        # Scene type options
        # Options: "interior", "exterior", "unrealistic_synthetic", "complex_others"
        self.scene_type = "interior"
        
        # Major light sources
        self.sunlight_source = False
        self.moonlight_source = False
        self.firelight_source = False
        self.artificial_light_source = False
        self.non_visible_light_source = False
        self.abstract_light_source = False
        self.complex_changing_light_source = False
        
        # Sunlight level
        self.sunlight_level = "unknown"  # Options: "normal", "sunny", "overcast", "sunset_sunrise", "unknown"
        
        # Light quality
        self.light_quality = "soft_diffused_light"  # Options: "hard_light", "soft_diffused_light", "complex_changing", "complex_contrasting", "complex_others"
        
        # Lighting setup description
        self.lighting_setup_description = ""
        
        # Contrast ratio on subject
        self.subject_contrast_ratio = "unknown"  # Options: "high_contrast", "normal_contrast", "minimal_contrast", "complex_changing", "unknown"
        
        # Direction of major light on subject
        self.subject_back_light = False
        self.subject_front_light = False
        self.subject_top_light = False
        self.subject_bottom_light = False
        self.subject_side_light = False
        self.subject_ambient_light = False
        
        # Special lighting effects on subject
        self.portrait_lighting = False
        self.rembrandt_lighting = False
        # below two are actually not dependent on whether the subject is present or not
        self.silhouette = False
        self.rim_light = False
        
        # Subject lighting description
        self.subject_lighting_description = ""
        
        # Lens and optical effects
        self.lens_flares_regular = False
        self.lens_flares_anamorphic = False
        self.mist_diffusion = False
        self.bokeh = False
        
        # Reflection lights
        self.reflection_from_water = False
        self.reflection_from_glossy_surface = False
        self.reflection_from_mirror = False
        
        # Special natural lighting effects
        self.rainbow = False
        self.heat_haze = False
        self.aurora = False
        self.aerial_perspective = False
        self.lightning = False
        
        # Special lighting effects on the scene
        self.colored_neon_lighting = False
        self.headlight_flashlight = False
        self.vignette = False
        self.water_caustics = False
        self.city_light = False
        self.street_light = False
        
        # Special lighting effects description
        self.special_lighting_description = ""
        
        # Volumetric lighting types
        self.volumetric_beam_light = False
        self.volumetric_spot_light = False
        self.god_rays = False
        self.light_through_medium = False
        self.volumetric_light_others = False
        
        # Volumetric lighting description
        self.volumetric_lighting_description = ""
        
        # Shadow pattern or Gobo lighting
        self.venetian_blinds = False
        self.subject_shape = False
        self.window_frames = False
        self.foliage = False
        self.shadow_patterns_gobo_others = False
        
        # Shadow pattern description
        self.shadow_pattern_description = ""
        
        # Lighting dynamics
        self.color_shifting_smooth = False
        self.color_shifting_sudden = False
        self.pulsing_flickering = False
        self.flashing = False
        self.moving_light = False
        
        # Lighting dynamics description
        self.lighting_dynamics_description = ""
        
        # Dynamic effects
        self.revealing_shot = False
        self.transformation_morphing = False
        self.levitation_floating = False
        self.explosion = False
        self.shattering_breaking = False
        self.diffusion = False
        self.splashing_waves = False
    
    def set_lighting_setup_attributes(self):
        self._set_color_grading_attributes()
        self._set_lighting_setup_attributes()
        self._set_subject_lighting_attributes()
        self._set_special_lighting_attributes()
        self._set_volumetric_lighting_attributes()
        self._set_shadow_pattern_attributes()
    
    def _set_color_grading_attributes(self):
        self.is_color_grading_complex = any([
            self.color_temperature in ["complex_changing", "complex_contrasting", "complex_others"], \
            self.color_saturation in ["complex_changing", "complex_contrasting", "complex_others"], \
            self.brightness in ["complex_changing", "complex_contrasting", "complex_others"]])

        self.is_black_white = self.color_saturation == "black_white" and self.color_temperature == "black_white"
        self.is_brighter_than_normal = self.brightness in ["very_bright", "bright"]
        self.is_darker_than_normal = self.brightness in ["dark", "very_dark"]
    
    def _set_lighting_setup_attributes(self):
        self.is_lighting_quality_complex = self.light_quality in ["complex_changing", "complex_contrasting", "complex_others"]
    
    def _set_subject_lighting_attributes(self):
        self.is_subject_lighting_applicable = self.subject_contrast_ratio == "unknown"
    
    def _set_special_lighting_attributes(self):
        self.lens_flares = self.lens_flares_regular or self.lens_flares_anamorphic
        
    def _set_volumetric_lighting_attributes(self):
        self.has_volumetric_lighting = self.volumetric_beam_light or self.volumetric_spot_light or self.god_rays or self.light_through_medium or self.volumetric_light_others
    
    def _set_shadow_pattern_attributes(self):
        self.has_shadow_patterns = self.venetian_blinds or self.subject_shape or self.window_frames or self.foliage or self.shadow_patterns_gobo_others
        
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
    
    def set_color_saturation(self, color_saturation):
        if color_saturation in ["high_saturation", "neutral", "low_saturation", "black_white", "complex_changing", "complex_contrasting", "complex_others"]:
            self.color_saturation = color_saturation
        else:
            raise ValueError("color_saturation must be one of 'high_saturation', 'neutral', 'low_saturation', 'black_white', 'complex_changing', 'complex_contrasting', 'complex_others'")
    
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
        if light_quality in ["hard_light", "soft_diffused_light", "complex_changing", "complex_contrasting", "complex_others"]:
            self.light_quality = light_quality
        else:
            raise ValueError("light_quality must be one of 'hard_light', 'soft_diffused_light', 'complex_changing', 'complex_contrasting', 'complex_others'")
    
    def set_subject_contrast_ratio(self, subject_contrast_ratio):
        if subject_contrast_ratio in ["high_contrast", "normal_contrast", "minimal_contrast", "complex_changing", "unknown"]:
            self.subject_contrast_ratio = subject_contrast_ratio
        else:
            raise ValueError("subject_contrast_ratio must be one of 'high_contrast', 'normal_contrast', 'minimal_contrast', 'complex_changing', 'unknown'")
    
    def set_sunlight_source(self, sunlight_source):
        if isinstance(sunlight_source, bool):
            self.sunlight_source = sunlight_source
        else:
            raise ValueError("sunlight_source must be a boolean value")
    
    def set_moonlight_source(self, moonlight_source):
        if isinstance(moonlight_source, bool):
            self.moonlight_source = moonlight_source
        else:
            raise ValueError("moonlight_source must be a boolean value")
    
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
    
    def set_abstract_light_source(self, abstract_light_source):
        if isinstance(abstract_light_source, bool):
            self.abstract_light_source = abstract_light_source
        else:
            raise ValueError("abstract_light_source must be a boolean value")
    
    def set_complex_changing_light_source(self, complex_changing_light_source):
        if isinstance(complex_changing_light_source, bool):
            self.complex_changing_light_source = complex_changing_light_source
        else:
            raise ValueError("complex_changing_light_source must be a boolean value")
    
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
    
    def set_subject_side_light(self, subject_side_light):
        if isinstance(subject_side_light, bool):
            self.subject_side_light = subject_side_light
        else:
            raise ValueError("subject_side_light must be a boolean value")
    
    def set_subject_ambient_light(self, subject_ambient_light):
        if isinstance(subject_ambient_light, bool):
            self.subject_ambient_light = subject_ambient_light
        else:
            raise ValueError("subject_ambient_light must be a boolean value")
    
    def set_portrait_lighting(self, portrait_lighting):
        if isinstance(portrait_lighting, bool):
            self.portrait_lighting = portrait_lighting
        else:
            raise ValueError("portrait_lighting must be a boolean value")
    
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
        if self.shot_transition:
            return # No need to verify other fields if shot transition is present
        
        complex_reasons = ["complex_changing", "complex_contrasting", "complex_others"]
        # if any([self.color_temperature in complex_reasons, self.color_saturation in complex_reasons, self.brightness in complex_reasons]):
        #     if not self.color_grading_description:
        #         raise ValueError("color_grading_description must be provided for complex color grading")
        if self.color_temperature == "black_white":
            if not self.color_saturation == "black_white":
                raise ValueError("color_saturation must be 'black_white' if color_temperature is 'black_white'")
        
        if self.abstract_light_source:
            if any([self.sunlight_source, self.moonlight_source, self.firelight_source, self.artificial_light_source, self.non_visible_light_source]):
                raise ValueError("abstract_light_source cannot be combined with other light sources")
        
        if self.sunlight_source:
            if self.sunlight_level == "unknown":
                raise ValueError("sunlight_level must be specified for sunlight source")
        else:
            if self.sunlight_level != "unknown":
                raise ValueError("sunlight_level must be 'unknown' if sunlight source is not present")
        
        if self.subject_contrast_ratio == "unknown":
            if any([self.subject_back_light, self.subject_front_light, self.subject_top_light, self.subject_bottom_light, self.subject_side_light, \
                self.subject_ambient_light, self.portrait_lighting, self.rembrandt_lighting]):
                raise ValueError("subject_contrast_ratio must be specified if subject lighting is present")

lighting_setup_params_demo = {
    "shot_transition": False,
    "color_temperature": "cool",
    "color_saturation": "high_saturation",
    "brightness": "very_bright",
    "color_grading_description": "Cool tones with high saturation and bright lighting",
    "scene_type": "interior",
    "sunlight_source": True,
    "moonlight_source": False,
    "firelight_source": False,
    "artificial_light_source": False,
    "non_visible_light_source": False,
    "abstract_light_source": False,
    "complex_changing_light_source": False,
    "sunlight_level": "sunny",
    "light_quality": "soft_diffused_light",
    "lighting_setup_description": "Soft diffused light with sunny outdoor setting",
    "subject_contrast_ratio": "high_contrast",
    "subject_back_light": True,
    "subject_front_light": False,
    "subject_top_light": False,
    "subject_bottom_light": False,
    "subject_side_light": False,
    "subject_ambient_light": False,
    "portrait_lighting": True,
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
    