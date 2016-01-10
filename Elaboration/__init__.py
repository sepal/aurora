# Use ElaborationConfig as a specific AppConfig for Elaborations
# to register the post_save signal to send the elaboration
# to plagcheck.
default_app_config = 'Elaboration.config.ElaborationConfig'
