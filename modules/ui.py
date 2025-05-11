from shiny import ui
from modules.ethics import get_ethics_questions


# Define CSS for better styling with mobile responsiveness
def get_custom_css():
    """Returns the custom CSS for the application"""

    # Base styles
    base_css = """
    /* Base styles */
    .title-box {
        text-align: center;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
    }

    .module-description {
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 0;
        color: #2C3E50;
    }

    .plot-title {
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 15px;
        color: #2C3E50;
    }

    .plot-container {
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 15px;
        background-color: #ffffff;
    }

    /* Add extra bottom padding for plot container to fix cut-off label */
    .plot-container-extra-bottom {
        padding-bottom: 50px !important;
    }

    .interpretation-box {
        margin-top: 20px;
        background-color: #E8F4FD;
        border-radius: 5px;
        padding: 15px;
        border-left: 5px solid #3498DB;
    }

    .interpretation-box pre {
        font-family: inherit;
        white-space: pre-wrap;
        margin: 0;
        font-size: 14px;
        line-height: 1.4;
    }

    .btn-resim {
        background-color: #3498DB;
        border-color: #2980B9;
        color: white;
        font-weight: bold;
        width: 100%;
    }

    .btn-resim:hover {
        background-color: #2980B9;
    }

    .seed-info {
        font-style: italic;
        font-size: 12px;
        color: #666;
        margin-top: 5px;
    }

    .center-button {
        text-align: center;
    }

    .driver-labels {
        font-weight: bold;
        color: #2C3E50;
    }

    /* Toggle Switch Styling */
    .toggle-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 15px 0;
    }

    .toggle-title {
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 16px;
        color: #2C3E50;
    }

    .switch-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    .switch-label {
        font-weight: bold;
        font-size: 18px;
        color: #7f8c8d;
        padding: 0 15px;
        cursor: pointer;
    }

    .switch-label.active {
        color: #2C3E50;
    }

    .switch {
        position: relative;
        display: inline-block;
        width: 80px;
        height: 40px;
    }

    .switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }

    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        transition: .4s;
        border-radius: 34px;
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 32px;
        width: 32px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: .4s;
        border-radius: 50%;
    }

    input:checked + .slider {
        background-color: #9B59B6; /* Purple for Kendrick */
    }

    input:not(:checked) + .slider {
        background-color: #3498DB; /* Blue for Drake */
    }

    input:focus + .slider {
        box-shadow: 0 0 1px #2196F3;
    }

    input:checked + .slider:before {
        transform: translateX(40px);
    }

    /* Rounded sliders */
    .slider.round {
        border-radius: 34px;
    }

    .slider.round:before {
        border-radius: 50%;
    }

    /* Make Drake blue and Kendrick purple */
    .drake-label {
        color: #3498DB;
    }

    .kendrick-label {
        color: #9B59B6;
    }

    .drake-label.active {
        font-weight: bold;
        text-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
    }

    .kendrick-label.active {
        font-weight: bold;
        text-shadow: 0 0 5px rgba(155, 89, 182, 0.5);
    }

    /* Highlight for premium difference */
    .premium-diff-highlight {
        background: linear-gradient(to right, #3498DB, #9B59B6);
        color: white;
        padding: 8px 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        font-weight: bold;
        text-align: center;
        margin: 10px auto;
        max-width: 80%;
    }

    /* Highlight for "Using values from" text */
    .values-from-highlight {
        background-color: #3498DB;
        color: white;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin: 10px auto 20px auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 80%;
        max-width: 600px;
    }

    /* Value display text */
    .value-display {
        font-weight: bold;
        color: #2C3E50;
        font-size: 16px;
    }

    /* Ethics tab styling */
    .ethics-container {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .ethics-intro {
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    .ethics-question {
        background-color: #E8F4FD;
        border-left: 5px solid #3498DB;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }

    .ethics-question p {
        white-space: normal;  /* Fix for wrapping issues */
        word-wrap: break-word;
        margin-bottom: 10px;
    }

    .ethics-question-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
        color: #2C3E50;
    }

    .ethical-variable {
        background-color: rgba(46, 204, 113, 0.2);
        border-left: 5px solid #2ECC71;
    }

    .unethical-variable {
        background-color: rgba(231, 76, 60, 0.2);
        border-left: 5px solid #E74C3C;
    }

    .ethics-grade {
        background-color: #E8F8F5;
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid #2ECC71;
        text-align: center;
    }

    .ethics-grade h3 {
        margin-top: 0;
        color: #2C3E50;
    }

    .ethics-grade span {
        font-size: 24px;
        font-weight: bold;
        color: #2ECC71;
    }

    .ethics-feedback {
        margin-top: 10px;
        font-style: italic;
    }

    .grade-btn {
        background-color: #2ECC71;
        border-color: #27AE60;
        color: white;
        font-weight: bold;
        margin-top: 15px;
    }

    .grade-btn:hover {
        background-color: #27AE60;
    }
    """

    # Additional mobile-specific CSS for navigation
    mobile_nav_css = """
    /* MOBILE RESPONSIVE STYLES */
    @media (max-width: 768px) {
        /* Text size adjustments */
        .plot-title {
            font-size: 18px !important;
        }
        .module-description {
            font-size: 14px !important;
        }
        .interpretation-box pre {
            font-size: 14px !important;
        }
        .toggle-title {
            font-size: 14px !important;
        }
        .switch-label {
            font-size: 16px !important;
            padding: 0 8px;
        }
        .value-display {
            font-size: 14px !important;
        }

        /* Stack columns vertically */
        .row > [class*="col-"] {
            width: 100%;
            margin-bottom: 15px;
        }

        /* Increase touch targets */
        .btn-resim, .switch-label, input[type="checkbox"] {
            min-height: 44px;
        }
        .slider:before {
            height: 32px;
            width: 32px;
        }

        /* Improve tab navigation */
        .nav-tabs {
            display: flex;
            overflow-x: auto;
            white-space: nowrap;
            border-bottom: none;
        }
        .nav-tabs > li {
            float: none;
            display: inline-block;
        }
        .nav-tabs > li > a {
            padding: 12px 8px;
            font-size: 14px;
        }

        /* Make plot containers more mobile-friendly */
        .plot-container {
            padding: 8px;
            margin-bottom: 15px;
        }

        /* Make ethics questions more compact */
        .ethics-question {
            padding: 10px;
            margin-bottom: 10px;
        }
        .ethics-question-title {
            font-size: 16px;
        }

        /* Make sliders more touch-friendly */
        .form-group {
            margin-bottom: 20px;
        }
        .irs-handle {
            width: 24px !important;
            height: 24px !important;
        }

        /* More compact header */
        h1 {
            font-size: 24px !important;
            margin-top: 10px !important;
            margin-bottom: 5px !important;
        }
        .title-box {
            padding: 5px !important;
            margin-bottom: 10px !important;
        }

        /* Mobile navigation tabs */
        .nav-tabs {
            display: flex;
            overflow-x: auto;
            white-space: nowrap;
            padding-bottom: 5px;
        }
        .nav-tabs > li {
            float: none;
            display: inline-block;
        }
        .nav-tabs > li > a {
            padding: 10px 8px;
            font-size: 14px;
        }

        /* Adjust widget padding and spacing */
        .form-group {
            margin-bottom: 10px !important;
        }
        .form-control {
            height: 44px; /* More touch-friendly input height */
        }
        .shiny-input-container {
            margin-bottom: 10px !important;
        }

        /* Improve seed info display */
        .seed-info {
            text-align: center !important;
            margin-top: 2px !important;
            margin-bottom: 5px !important;
        }
    }
    """

    # Mobile-specific CSS for better visualization and interaction
    mobile_optimized_css = """
    /* Mobile-friendly plot containers */
    .mobile-friendly-plot {
        padding: 8px !important;
        margin-bottom: 10px !important;
        min-height: 500px !important;  /* Reduced from 700px */
    }

    /* HORIZONTAL SCROLLING for charts */
    .scrollable-plot-container {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important; 
        max-width: 100% !important;
        white-space: nowrap !important;
        padding: 5px 0 !important;
    }

    /* Make sure plots maintain size within scrollable container */
    .scrollable-plot-container .shiny-plot-output {
        display: inline-block !important;
        min-width: 200% !important; /* Decreased from 250% */
        max-width: none !important; /* Remove any max-width constraints */
        height: auto !important; /* Height will scale with width */
    }

    /* Enhance the scroll indicator to make it more noticeable */
    .scroll-indicator {
        text-align: center;
        font-size: 14px !important;
        font-style: italic;
        color: #3498DB;
        margin: 0 0 15px 0;
        padding: 5px;
        background-color: #F8F9FA;
        border-radius: 5px;
        border: 1px dashed #BDC3C7;
    }

    /* Larger mobile button */
    .mobile-button {
        height: 60px !important;
        font-size: 20px !important;
        margin: 15px 0 !important;
        border-radius: 10px !important;
    }

    /* Mobile interpretation box */
    .mobile-interpretation {
        font-size: 16px !important;
        padding: 15px !important;
        line-height: 1.5 !important;
        border-radius: 10px !important;
        border-left-width: 8px !important;
    }

    .mobile-interpretation pre {
        font-size: 16px !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        font-family: system-ui, -apple-system, sans-serif !important;
    }

    /* Better spacing between UI elements on mobile */
    @media (max-width: 768px) {
        /* General spacing and sizing */
        .shiny-input-container {
            margin-bottom: 20px !important;
        }

        .form-group {
            margin-bottom: 25px !important;
        }

        .module-description {
            font-size: 16px !important;
            padding: 10px !important;
            margin-bottom: 15px !important;
        }

        .plot-title {
            font-size: 18px !important;
            margin-bottom: 10px !important;
        }

        /* Improved slider appearance */
        .irs {
            height: 70px !important;
        }

        .irs-min, .irs-max, .irs-single, .irs-from, .irs-to {
            font-size: 14px !important;
            padding: 4px 8px !important;
            border-radius: 6px !important;
        }

        .irs-handle {
            width: 30px !important;
            height: 30px !important;
            top: 22px !important;
        }

        .irs-bar {
            height: 10px !important;
            top: 32px !important;
        }

        .irs-line {
            height: 10px !important;
            top: 32px !important;
        }

        /* Fix cut-off labels */
        .plot-container {
            padding-bottom: 40px !important;
            margin-bottom: 25px !important;
        }

        /* Adjust padding within plot containers for better use of space */
        .plot-container {
            padding: 12px 5px !important;
        }

        /* Tab navigation */
        .nav-tabs > li > a {
            font-size: 16px !important;
            padding: 15px 10px !important;
        }

        /* Seed info display */
        .seed-info {
            font-size: 14px !important;
            margin: 5px 0 15px 0 !important;
        }

        /* Improved section spacing */
        .title-box {
            margin-bottom: 20px !important;
        }

        hr {
            margin: 25px 0 !important;
        }

        /* Fix for collapsed/flattened plot heights */
        .scrollable-plot-container {
            min-height: 500px !important;  /* Reduced from 700px */
            height: auto !important;
        }

        /* Set constraints on the plot images themselves */
        .shiny-plot-output img {
            min-height: 500px !important;  /* Reduced from 700px */
            height: auto !important;
            max-width: 200% !important;  /* Decreased from 250% */
        }
    }

    /* Make touch scrolling more obvious with a subtle gradient indicator */
    .scrollable-plot-container:after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        height: 100%;
        width: 30px;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.8));
        pointer-events: none;
    }
    """

    # Combine all CSS
    return base_css + mobile_nav_css + mobile_optimized_css


# Custom toggle switch HTML with larger touch targets for mobile
def driver_toggle_switch():
    """Returns the custom toggle switch UI element for driver selection"""
    return ui.div(
        {"class": "toggle-container"},
        ui.div({"class": "toggle-title"}, "Select Low Risk Driver:"),
        ui.div(
            {"class": "switch-container"},
            ui.div({"class": "switch-label drake-label active", "id": "drake-label",
                    "onclick": "document.getElementById('toggle_driver').checked = false; $(document).trigger('shiny:inputchanged'); updateLabels();"},
                   "Drake"),
            ui.div(
                {"class": "switch"},
                ui.tags.input(
                    {"type": "checkbox", "id": "toggle_driver", "name": "selected_good_driver", "value": "kendrick",
                     "onchange": "updateLabels();"}),
                ui.tags.label({"for": "toggle_driver", "class": "slider round"})
            ),
            ui.div({"class": "switch-label kendrick-label", "id": "kendrick-label",
                    "onclick": "document.getElementById('toggle_driver').checked = true; $(document).trigger('shiny:inputchanged'); updateLabels();"},
                   "Kendrick")
        ),
        # Add JavaScript to handle the toggle and label styling
        ui.tags.script("""
        function updateLabels() {
            if($("#toggle_driver").is(":checked")) {
                // Kendrick is selected
                $("#drake-label").removeClass("active");
                $("#kendrick-label").addClass("active");
                Shiny.setInputValue("selected_good_driver", "kendrick");
            } else {
                // Drake is selected
                $("#drake-label").addClass("active");
                $("#kendrick-label").removeClass("active");
                Shiny.setInputValue("selected_good_driver", "drake");
            }
        }

        $(document).ready(function() {
            // Set initial state
            updateLabels();

            // Make sure slider click works
            $(".slider").click(function(e) {
                // Don't let event bubble up to prevent double-toggling
                e.stopPropagation();
            });
        });
        """)
    )


# Add device detection JavaScript
def get_device_detection_js():
    """Returns JavaScript for device detection"""
    return """
    $(document).ready(function() {
        function detectMobile() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        }

        // Set the isMobile input value
        Shiny.setInputValue('isMobile', detectMobile());

        // Also set viewport for better mobile rendering
        if (detectMobile()) {
            $('meta[name=viewport]').attr('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
        }
    });
    """


# Script to enforce plot heights
def get_enforce_plot_height_js():
    """Returns JavaScript to enforce plot heights"""
    return """
    $(document).ready(function() {
        // Force plots to maintain their height
        function enforcePlotHeight() {
            // Set explicit heights for plot containers
            $(".shiny-plot-output").each(function() {
                var height = $(this).attr('height');
                if (height) {
                    $(this).css('min-height', height);
                    // Also set height on the actual image
                    $(this).find('img').css('min-height', height);
                }
            });
        }

        // Run initially and whenever plots are updated
        enforcePlotHeight();
        $(document).on('shiny:value', function(event) {
            if (event.name.indexOf('_plot') > -1) {
                setTimeout(enforcePlotHeight, 100);
            }
        });
    });
    """


# Build JavaScript for ethics module
def get_ethics_js():
    """Returns JavaScript for the ethics module"""
    return """
    $(document).ready(function() {
        $('#grade_ethics').click(function() {
            // Wait a moment for the grade to be calculated
            setTimeout(function() {
                // Remove any existing coloring
                $('.ethics-question').removeClass('ethical-variable unethical-variable');

                // Color the blocks based on correct answers
                $('#drake_rating_block').addClass('unethical-variable');
                $('#kendrick_rating_block').addClass('unethical-variable');
                $('#age_rating_block').addClass('ethical-variable');
                $('#vehicle_rating_block').addClass('ethical-variable');
                $('#religion_rating_block').addClass('unethical-variable');
                $('#race_rating_block').addClass('unethical-variable');
                $('#experience_rating_block').addClass('ethical-variable');
                $('#multiproduct_rating_block').addClass('ethical-variable');
                $('#speeding_rating_block').addClass('ethical-variable');
                $('#driving_rating_block').addClass('ethical-variable');
            }, 500);
        });
    });
    """


# Risk Pooling Module UI
def get_risk_pooling_ui():
    """Returns the UI for the Risk Pooling module"""
    return ui.nav_panel("1. Risk Pooling",
                        # Title in its own row
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "title-box"},
                                             ui.div({"class": "module-description"},
                                                    "How insurance spreads risk across many people"
                                                    )
                                             )
                                      )
                        ),

                        # Mobile-optimized sliders - one per row for better touch targets
                        ui.row(
                            ui.column(12,
                                      ui.input_slider("accident_probability", "Accident Probability:",
                                                      min=0.01, max=0.25, value=0.05, step=0.01)
                                      )
                        ),
                        ui.row(
                            ui.column(12,
                                      ui.input_slider("num_policyholders", "Number of Policyholders:",
                                                      min=10, max=1000, value=100, step=10)
                                      )
                        ),

                        # Large, easy-to-tap button
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "center-button"},
                                             ui.input_action_button("resim_risk", "Re-simulate",
                                                                    class_="btn-resim btn-lg mobile-button")
                                             )
                                      )
                        ),

                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "seed-info", "style": "text-align: center;"},
                                             ui.output_text("risk_seed_info"))
                                      )
                        ),

                        # Main content - Direct height fix with reduced pixel height
                        ui.hr(),
                        ui.div({"class": "plot-container"},
                               ui.div({"class": "plot-title"}, "Risk Pooling Visualization"),
                               ui.div(
                                   {
                                       "style": "text-align: center; color: #666; font-style: italic; margin-bottom: 10px;"},
                                   "← Swipe horizontally to explore the full chart →"),
                               ui.div(
                                   {
                                       "style": "overflow-x: auto; -webkit-overflow-scrolling: touch; position: relative;"},
                                   ui.output_plot("risk_pooling_plot",
                                                  width="200%",
                                                  height="500px")  # Reduced height
                               )
                               ),
                        ui.div({"class": "interpretation-box mobile-interpretation"},
                               ui.tags.pre(ui.output_text("risk_pooling_interpretation"))
                               )
                        )


# Driver Comparison Module UI
def get_driver_comparison_ui():
    """Returns the UI for the Driver Comparison module"""
    return ui.nav_panel("2. Driver Comparison",
                        # Title in its own row
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "title-box"},
                                             ui.div({"class": "module-description"},
                                                    "Frequency and severity create distinct risk clusters."
                                                    )
                                             )
                                      )
                        ),
                        # Driver selection toggle switch
                        ui.row(
                            ui.column(12, driver_toggle_switch())
                        ),
                        # Sliders in mobile-friendly vertical layout
                        ui.row(
                            ui.column(6,
                                      ui.input_slider("base_frequency", "Accident Freq (Low Risk):",
                                                      min=0.01, max=0.10, value=0.03, step=0.01)
                                      ),
                            ui.column(6,
                                      ui.input_slider("base_severity", "Claim Amt (Low Risk):",
                                                      min=2000, max=10000, value=5000, step=500)
                                      )
                        ),
                        ui.row(
                            ui.column(6,
                                      ui.div({"class": "driver-labels"},
                                             ui.output_text("bad_driver_freq_label")),
                                      ui.input_slider("freq_multiplier", "",
                                                      min=1.5, max=5.0, value=3.0, step=0.5)
                                      ),
                            ui.column(6,
                                      ui.div({"class": "driver-labels"},
                                             ui.output_text("bad_driver_severity_label")),
                                      ui.input_slider("severity_multiplier", "",
                                                      min=1.2, max=3.0, value=2.0, step=0.2)
                                      )
                        ),
                        # Re-simulate button
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "center-button"},
                                             ui.input_action_button("resim_drivers", "Re-simulate",
                                                                    class_="btn-resim mobile-button")
                                             )
                                      )
                        ),
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "seed-info", "style": "text-align: center;"},
                                             ui.output_text("driver_seed_info")
                                             )
                                      )
                        ),
                        ui.hr(),
                        # Main content with direct height fix
                        ui.div({"class": "plot-container"},
                               ui.div({"class": "plot-title"}, "Driver Risk Profiles"),
                               ui.div(
                                   {
                                       "style": "text-align: center; color: #666; font-style: italic; margin-bottom: 10px;"},
                                   "← Swipe horizontally to explore the full chart →"),
                               ui.div(
                                   {
                                       "style": "overflow-x: auto; -webkit-overflow-scrolling: touch; position: relative;"},
                                   ui.output_plot("driver_comparison_plot",
                                                  width="150%",  # Further reduced from 200% to 150%
                                                  height="500px")
                               )
                               ),
                        ui.div({"class": "interpretation-box mobile-interpretation"},
                               ui.tags.pre(ui.output_text("driver_comparison_interpretation"))
                               )
                        )


# Premium Calculation Module UI
def get_premium_calculation_ui():
    """Returns the UI for the Premium Calculation module"""
    return ui.nav_panel("3. Premium Calculation",
                        # Title in its own row
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "title-box"},
                                             ui.div({"class": "module-description"},
                                                    "Insurance premiums based on frequency, severity & more."
                                                    )
                                             )
                                      )
                        ),
                        # Output text showing we're using values from previous tab
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "values-from-highlight"},
                                             "Using values from Driver Comparison tab"
                                             )
                                      )
                        ),
                        # Information about the inherited values - simplified for mobile
                        ui.row(
                            ui.column(6,
                                      ui.div({"style": "text-align: center;"},
                                             ui.output_ui("premium_first_cohort_label"),
                                             ui.br(),
                                             ui.div({"class": "value-display"},
                                                    ui.output_text("premium_good_driver_info"))
                                             )
                                      ),
                            ui.column(6,
                                      ui.div({"style": "text-align: center;"},
                                             ui.output_ui("premium_bad_driver_label"),
                                             ui.br(),
                                             ui.div({"class": "value-display"},
                                                    ui.output_text("premium_bad_info"))
                                             )
                                      )
                        ),
                        ui.row(
                            ui.column(6,
                                      ui.div({"style": "text-align: center;"},
                                             ui.strong("Est. Frequency:"),
                                             ui.br(),
                                             ui.div({"class": "value-display"},
                                                    ui.output_text("premium_good_freq_info"))
                                             )
                                      ),
                            ui.column(6,
                                      ui.div({"style": "text-align: center;"},
                                             ui.strong("Est. Severity:"),
                                             ui.br(),
                                             ui.div({"class": "value-display"},
                                                    ui.output_text("premium_good_severity_info"))
                                             )
                                      )
                        ),
                        ui.hr(),
                        # Main content with direct height fix
                        ui.div({"class": "plot-container"},
                               ui.div({"class": "plot-title"}, "Premium Components"),
                               ui.div(
                                   {
                                       "style": "text-align: center; color: #666; font-style: italic; margin-bottom: 10px;"},
                                   "← Swipe horizontally to explore the full chart →"),
                               ui.div(
                                   {
                                       "style": "overflow-x: auto; -webkit-overflow-scrolling: touch; position: relative;"},
                                   ui.output_plot("premium_calc_plot",
                                                  width="200%",
                                                  height="800px")  # Reduced height
                               )
                               ),
                        ui.div({"class": "interpretation-box mobile-interpretation"},
                               ui.tags.pre(ui.output_text("premium_calc_interpretation"))
                               )
                        )


# Ethics of Rating Module UI
def get_ethics_ui():
    """Returns the UI for the Ethics of Rating module"""
    ethics_questions = get_ethics_questions()

    # Create question rows
    question_rows = []
    for question in ethics_questions:
        question_rows.append(
            ui.row(
                ui.column(12,
                          ui.div({"class": "ethics-question", "id": f"{question['id']}_block"},
                                 ui.div({"class": "ethics-question-title"}, question["title"]),
                                 ui.input_checkbox(question["id"], "Appropriate to use as a rating variable",
                                                   value=False)
                                 )
                          )
            )
        )

    # Create the full UI
    return ui.nav_panel("4. Ethics of Rating",
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "title-box"},
                                             ui.div({"class": "module-description"},
                                                    "Ethical considerations in insurance rating."
                                                    )
                                             )
                                      )
                        ),
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "ethics-container"},
                                             ui.div({"class": "ethics-intro"},
                                                    """
                                                    Insurance pricing relies on risk factors that predict future claims. 
                                                    Not all potential rating variables are acceptable for use.
                            
                                                    For each item below, indicate if it would be appropriate to use
                                                    in setting auto insurance rates.
                                                    """
                                                    )
                                             )
                                      )
                        ),
                        # Add all question rows
                        *question_rows,
                        # Grade Button
                        ui.row(
                            ui.column(12,
                                      ui.div({"class": "center-button"},
                                             ui.input_action_button("grade_ethics", "Grade My Answers",
                                                                    class_="btn-resim grade-btn mobile-button")
                                             )
                                      )
                        ),
                        # Grade Results
                        ui.row(
                            ui.column(12, ui.output_ui("ethics_grade_output"))
                        ),
                        # Add JavaScript for color coding
                        ui.tags.script(get_ethics_js())
                        )


# Create the app UI
def get_app_ui():
    """Returns the complete UI for the application"""
    return ui.page_fluid(
        # Add viewport meta tag for mobile
        ui.tags.head(
            ui.tags.meta(
                name="viewport",
                content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
            ),
            ui.tags.style(get_custom_css()),
            ui.tags.script(get_device_detection_js()),
            ui.tags.script(get_enforce_plot_height_js())
        ),
        ui.h1("Insurance Fundamentals", style="text-align: center; margin-bottom: 10px;"),
        ui.p("Interactive demonstrations of key insurance concepts", style="text-align: center; margin-bottom: 20px;"),

        ui.navset_tab(
            # 1. RISK POOLING MODULE
            get_risk_pooling_ui(),

            # 2. DRIVER COMPARISON MODULE
            get_driver_comparison_ui(),

            # 3. PREMIUM CALCULATION MODULE
            get_premium_calculation_ui(),

            # 4. ETHICS OF RATING MODULE
            get_ethics_ui()
        )
    )