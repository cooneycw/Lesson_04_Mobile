from shiny import App, ui, render, reactive
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
import random
import time

# Import the demonstration modules - use mobile-optimized versions
from modules.risk_pooling import demonstrate_risk_pooling
from modules.driver_comparison import demonstrate_driver_comparison
from modules.premium_calculation import demonstrate_premium_calculation

# Define CSS for better styling with mobile responsiveness
custom_css = """
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
}
"""

# Additional mobile-specific CSS for navigation
mobile_nav_css = """
@media (max-width: 768px) {
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
    min-height: 700px !important;
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
    min-width: 250% !important; /* Increased from 150% to 250% for better readability */
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
        min-height: 700px !important;
        height: auto !important;
    }

    /* Set constraints on the plot images themselves */
    .shiny-plot-output img {
        min-height: 700px !important;
        height: auto !important;
        max-width: 250% !important;
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
custom_css = custom_css + mobile_nav_css + mobile_optimized_css


# Custom toggle switch HTML with larger touch targets for mobile
def driver_toggle_switch():
    # Create a custom toggle switch HTML with mobile improvements
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
device_detection_js = """
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
enforce_plot_height_js = """
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

# App UI - Modified for mobile responsiveness
app_ui = ui.page_fluid(
    # Add viewport meta tag for mobile
    ui.tags.head(
        ui.tags.meta(
            name="viewport",
            content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
        ),
        ui.tags.style(custom_css),
        ui.tags.script(device_detection_js),
        ui.tags.script(enforce_plot_height_js)
    ),
    ui.h1("Insurance Fundamentals", style="text-align: center; margin-bottom: 10px;"),
    ui.p("Interactive demonstrations of key insurance concepts", style="text-align: center; margin-bottom: 20px;"),

    ui.navset_tab(
        # 1. RISK POOLING MODULE - Mobile Optimized with direct height fix
        ui.nav_panel("1. Risk Pooling",
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

                     # Main content - Direct height fix with huge pixel height
                     ui.hr(),
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Risk Pooling Visualization"),
                            ui.div(
                                {"style": "text-align: center; color: #666; font-style: italic; margin-bottom: 10px;"},
                                "← Swipe horizontally to explore the full chart →"),
                            ui.div(
                                {"style": "overflow-x: auto; -webkit-overflow-scrolling: touch; position: relative;"},
                                ui.output_plot("risk_pooling_plot",
                                               width="250%",
                                               height="1000px")  # Fixed pixel height
                            )
                            ),
                     ui.div({"class": "interpretation-box mobile-interpretation"},
                            ui.tags.pre(ui.output_text("risk_pooling_interpretation"))
                            )
                     ),

        # 2. DRIVER COMPARISON MODULE - Mobile Optimized with direct height fix
        ui.nav_panel("2. Driver Comparison",
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
                                {"style": "text-align: center; color: #666; font-style: italic; margin-bottom: 10px;"},
                                "← Swipe horizontally to explore the full chart →"),
                            ui.div(
                                {"style": "overflow-x: auto; -webkit-overflow-scrolling: touch; position: relative;"},
                                ui.output_plot("driver_comparison_plot",
                                               width="250%",
                                               height="1000px")  # Fixed pixel height
                            )
                            ),
                     ui.div({"class": "interpretation-box mobile-interpretation"},
                            ui.tags.pre(ui.output_text("driver_comparison_interpretation"))
                            )
                     ),

        # 3. PREMIUM CALCULATION MODULE - Mobile Optimized with direct height fix
        ui.nav_panel("3. Premium Calculation",
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
                                {"style": "text-align: center; color: #666; font-style: italic; margin-bottom: 10px;"},
                                "← Swipe horizontally to explore the full chart →"),
                            ui.div(
                                {"style": "overflow-x: auto; -webkit-overflow-scrolling: touch; position: relative;"},
                                ui.output_plot("premium_calc_plot",
                                               width="250%",
                                               height="1200px")  # Fixed pixel height
                            )
                            ),
                     ui.div({"class": "interpretation-box mobile-interpretation"},
                            ui.tags.pre(ui.output_text("premium_calc_interpretation"))
                            )
                     ),

        # 4. ETHICS OF RATING MODULE - Mobile-friendly layout
        ui.nav_panel("4. Ethics of Rating",
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
                     # Condensed rating variables format for mobile
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "drake_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Drake Listeners"),
                                          ui.input_checkbox("drake_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "kendrick_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Kendrick Listeners"),
                                          ui.input_checkbox("kendrick_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "age_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Driver Age"),
                                          ui.input_checkbox("age_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "vehicle_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Vehicle Type"),
                                          ui.input_checkbox("vehicle_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "religion_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Religion"),
                                          ui.input_checkbox("religion_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "race_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Race/Ethnicity"),
                                          ui.input_checkbox("race_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "experience_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Years of Driving Experience"),
                                          ui.input_checkbox("experience_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "multiproduct_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Multi-Product Discount"),
                                          ui.input_checkbox("multiproduct_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "speeding_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Speeding Convictions"),
                                          ui.input_checkbox("speeding_rating",
                                                            "Appropriate to use as a rating variable", value=False)
                                          )
                                   )
                     ),
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "ethics-question", "id": "driving_rating_block"},
                                          ui.div({"class": "ethics-question-title"}, "Driving History"),
                                          ui.input_checkbox("driving_rating", "Appropriate to use as a rating variable",
                                                            value=False)
                                          )
                                   )
                     ),
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
                     # Add JavaScript for color coding - updated to replace gender with religion
                     ui.tags.script("""
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
            """)
                     )
    )
)


# Server logic - with mobile detection
def server(input, output, session):
    # Mobile detection reactive value
    is_mobile = reactive.Value(False)

    @reactive.Effect
    def _update_mobile_status():
        # Update the mobile status if "isMobile" input exists
        if hasattr(input, "isMobile"):
            is_mobile.set(input.isMobile())

    # Reactive values to track simulation offsets
    risk_sim_offset = reactive.Value(0)
    driver_sim_offset = reactive.Value(0)

    # Helper function to get the selected good driver
    @reactive.Calc
    def get_good_driver():
        # Get the value from the selected_good_driver input
        return input.selected_good_driver()

    # Helper function to get the bad driver name
    def get_bad_driver_name():
        good_driver = get_good_driver()
        return "Kendrick" if good_driver == "drake" else "Drake"

    # Update offset values when re-simulate buttons are clicked
    @reactive.Effect
    @reactive.event(input.resim_risk)
    def _update_risk_seed():
        new_offset = random.randint(1, 10000)
        risk_sim_offset.set(new_offset)
        print(f"Risk pooling seed offset updated to: {new_offset}")

    @reactive.Effect
    @reactive.event(input.resim_drivers)
    def _update_driver_seed():
        new_offset = random.randint(1, 10000)
        driver_sim_offset.set(new_offset)
        print(f"Driver comparison seed offset updated to: {new_offset}")

    # Dynamic labels for second cohort
    @output
    @render.text
    def bad_driver_freq_label():
        bad_driver = get_bad_driver_name()
        # Shorter text for mobile
        if is_mobile.get():
            return f"{bad_driver} Freq Mult:"
        else:
            return f"{bad_driver} Cohort Frequency Multiplier:"

    @output
    @render.text
    def bad_driver_severity_label():
        bad_driver = get_bad_driver_name()
        # Shorter text for mobile
        if is_mobile.get():
            return f"{bad_driver} Amount Mult:"
        else:
            return f"{bad_driver} Cohort Claim Amount Multiplier:"

    # Using render.ui for HTML content - now with specific cohort names
    @output
    @render.ui
    def premium_bad_driver_label():
        bad_driver = get_bad_driver_name()
        return ui.strong(f"{bad_driver} Cohort:")

    @output
    @render.ui
    def premium_first_cohort_label():
        good_driver = get_good_driver().capitalize()
        return ui.strong(f"{good_driver} Cohort:")

    # Reactive calculations for seed values
    @reactive.Calc
    def risk_seed():
        base_seed = int(input.accident_probability() * 10000 + input.num_policyholders())
        offset = risk_sim_offset.get()
        return base_seed + offset, base_seed, offset

    @reactive.Calc
    def driver_seed():
        base_seed = int(input.base_frequency() * 10000 + input.base_severity() +
                        input.freq_multiplier() * 100 + input.severity_multiplier() * 100)
        offset = driver_sim_offset.get()
        return base_seed + offset, base_seed, offset

    # Display seed info in UI
    @output
    @render.text
    def risk_seed_info():
        seed, base, offset = risk_seed()
        # Simplified for mobile
        if is_mobile.get():
            return f"Seed: {seed}"
        else:
            return f"Seed: {seed} (Base: {base}, Offset: {offset})"

    @output
    @render.text
    def driver_seed_info():
        seed, base, offset = driver_seed()
        # Simplified for mobile
        if is_mobile.get():
            return f"Seed: {seed}"
        else:
            return f"Seed: {seed} (Base: {base}, Offset: {offset})"

    # Risk Pooling Module
    @reactive.Calc
    def risk_data():
        seed, base, offset = risk_seed()
        print(f"Risk Pooling using seed: {seed} (base: {base}, offset: {offset})")
        return demonstrate_risk_pooling(
            input.accident_probability(),
            input.num_policyholders(),
            seed=seed,
            return_fig=True,
            is_mobile=is_mobile.get()  # Pass mobile flag
        )

    @output
    @render.plot
    def risk_pooling_plot():
        fig, _ = risk_data()
        return fig

    @output
    @render.text
    def risk_pooling_interpretation():
        _, stats = risk_data()
        claim_amount = 20000  # Fixed claim amount

        # Much shorter, focused interpretation for mobile
        if is_mobile.get():
            text = "KEY INSIGHTS:\n"
            text += f"• Risk: {input.accident_probability():.1%} chance of ${claim_amount:,.0f} loss\n"
            text += f"• Insurance: Everyone pays ${stats['fair_premium']:,.0f}\n"

            # Highlight the outcome clearly
            if stats['pool_performance'] < 1:
                text += f"• RESULT: Insurance had ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} SURPLUS\n"
            else:
                text += f"• RESULT: Insurance had ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} DEFICIT\n"

            text += f"• More policyholders = more stable results"
            return text
        else:
            # Original interpretation for desktop
            text = "Insurance Interpretation:\n"
            text += f"• Individual Risk: Each person has a {input.accident_probability():.1%} chance of a ${claim_amount:,.0f} loss.\n"
            text += f"• Without Insurance: {stats['num_with_loss']} people ({stats['percent_with_loss']:.1f}%) faced a ${claim_amount:,.0f} loss in this simulation.\n"
            text += f"• With Insurance: Everyone pays a premium of ${stats['fair_premium']:,.0f}.\n"
            text += f"• Risk Pooling Result: The insurer collected ${stats['pool_premium_total']:,.0f} and paid ${stats['total_losses']:,.0f} in claims.\n"

            if stats['pool_performance'] < 1:
                text += f"• This year the insurance pool had a ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} surplus.\n"
                text += "• The surplus can be held as capital to handle future years when claims exceed premiums.\n"
            else:
                text += f"• This year the insurance pool had a ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} deficit.\n"
                text += "• The deficit must be covered by the insurer's capital reserves.\n"

            text += f"• Key Insight: As the number of policyholders increases, the 'Actual/Expected' ratio approaches 1.0, "
            text += f"making the insurance pool's results more predictable and stable."

            return text

    # Driver Comparison Module
    @reactive.Calc
    def driver_data():
        seed, base, offset = driver_seed()
        good_driver = get_good_driver()
        good_driver_image = f"{good_driver}.jpeg"
        print(f"Driver Comparison using seed: {seed} (base: {base}, offset: {offset}, good driver: {good_driver})")
        return demonstrate_driver_comparison(
            input.base_frequency(),
            input.base_severity(),
            input.freq_multiplier(),
            input.severity_multiplier(),
            seed=seed,
            return_fig=True,
            good_driver_image=good_driver_image,
            is_mobile=is_mobile.get()  # Pass mobile flag
        )

    @output
    @render.plot
    def driver_comparison_plot():
        fig, _ = driver_data()
        return fig

    @output
    @render.text
    def driver_comparison_interpretation():
        _, stats = driver_data()
        good_driver = get_good_driver().capitalize()
        bad_driver = get_bad_driver_name()

        # Use specific cohort names
        first_cohort = f"{good_driver} Cohort"
        second_cohort = f"{bad_driver} Cohort"

        # Shorter interpretation for mobile
        if is_mobile.get():
            text = "Risk Profile Summary:\n"
            text += f"• {first_cohort}: {stats['good_avg_frequency']:.1%} freq, ${stats['good_avg_severity']:,.0f} severity\n"
            text += f"• {second_cohort}: {stats['bad_avg_frequency']:.1%} freq, ${stats['bad_avg_severity']:,.0f} severity\n\n"
            text += f"• {second_cohort} has {stats['freq_multiplier']:.1f}x higher accident frequency\n"
            text += f"• {second_cohort}'s claims are {stats['severity_multiplier']:.1f}x more costly\n\n"
            text += f"• Expected Loss - {first_cohort}: ${stats['good_avg_frequency'] * stats['good_avg_severity']:,.0f}\n"
            text += f"• Expected Loss - {second_cohort}: ${stats['bad_avg_frequency'] * stats['bad_avg_severity']:,.0f}\n"
            text += f"• Risk Difference: {stats['loss_multiplier']:.1f}x more expected losses\n"

            return text
        else:
            # Original interpretation
            text = "Risk Profile Interpretation:\n"
            text += f"• {first_cohort} has an est. accident frequency of {stats['good_avg_frequency']:.1%} and an est. average claim amount of ${stats['good_avg_severity']:,.0f}\n"
            text += f"• {second_cohort} has an est. accident frequency of {stats['bad_avg_frequency']:.1%} and an est. average claim amount of ${stats['bad_avg_severity']:,.0f}\n\n"

            text += f"• Frequency Difference: {second_cohort} has {stats['freq_multiplier']:.1f}x more frequent accidents than {first_cohort}\n"
            text += f"• Claim Amount Difference: {second_cohort}'s claims are {stats['severity_multiplier']:.1f}x more costly than {first_cohort}'s claims\n\n"

            text += f"• Expected Annual Cost - {first_cohort}: ${stats['good_avg_frequency'] * stats['good_avg_severity']:,.0f} per driver\n"
            text += f"• Expected Annual Cost - {second_cohort}: ${stats['bad_avg_frequency'] * stats['bad_avg_severity']:,.0f} per driver\n"
            text += f"• Overall Risk Difference: {second_cohort} generates {stats['loss_multiplier']:.1f}x more in expected losses\n\n"

            text += "• Key Insight: The scatterplot illustrates why insurance companies segment drivers into risk cohorts.\n"
            text += "  Both frequency and claim amounts contribute to the overall cost differences between driver cohorts.\n"
            text += "  Each dot represents an individual driver's risk profile, showing natural variation within cohorts."

            return text

    # Display premium calculation tab info about inherited values
    @output
    @render.text
    def premium_good_driver_info():
        return f"{get_good_driver().capitalize()}"

    @output
    @render.text
    def premium_good_freq_info():
        _, stats = driver_data()
        return f"{stats['good_avg_frequency']:.1%}"

    @output
    @render.text
    def premium_good_severity_info():
        _, stats = driver_data()
        return f"${stats['good_avg_severity']:,.0f}"

    @output
    @render.text
    def premium_bad_info():
        _, stats = driver_data()
        # Simplified for mobile
        if is_mobile.get():
            return f"{stats['bad_avg_frequency']:.1%}, ${stats['bad_avg_severity']:,.0f}"
        else:
            return f"Freq: {stats['bad_avg_frequency']:.1%}, Severity: ${stats['bad_avg_severity']:,.0f}"

    # Premium Calculation Module - Now uses values from driver comparison
    @reactive.Calc
    def premium_calc_data():
        # Get driver data from previous tab
        _, driver_stats = driver_data()

        # Use the good and bad driver data from driver comparison
        good_freq = driver_stats['good_avg_frequency']
        good_severity = driver_stats['good_avg_severity']
        bad_freq = driver_stats['bad_avg_frequency']
        bad_severity = driver_stats['bad_avg_severity']
        good_driver = get_good_driver()
        good_driver_image = f"{good_driver}.jpeg"

        # Pass values to premium calculation with mobile flag
        return demonstrate_premium_calculation(
            accident_frequency=good_freq,
            claim_severity=good_severity,
            bad_driver_freq=bad_freq,
            bad_driver_severity=bad_severity,
            good_driver_image=good_driver_image,
            return_fig=True,
            is_mobile=is_mobile.get()  # Pass mobile flag
        )

    @output
    @render.plot
    def premium_calc_plot():
        fig, _ = premium_calc_data()
        return fig

    @output
    @render.text
    def premium_calc_interpretation():
        _, stats = premium_calc_data()
        _, driver_stats = driver_data()

        good_freq = driver_stats['good_avg_frequency']
        good_severity = driver_stats['good_avg_severity']
        bad_freq = driver_stats['bad_avg_frequency']
        bad_severity = driver_stats['bad_avg_severity']
        good_driver = get_good_driver().capitalize()
        bad_driver = get_bad_driver_name()

        # Use specific cohort names
        first_cohort = f"{good_driver} Cohort"
        second_cohort = f"{bad_driver} Cohort"

        expense_ratio = 0.25
        risk_margin_ratio = 0.05

        # Shorter interpretation for mobile
        if is_mobile.get():
            text = "Premium Comparison:\n"
            text += f"• {first_cohort}:\n"
            text += f"  - Expected Loss: ${stats['expected_loss']:,.0f}\n"
            text += f"  - Expenses: ${stats['expenses']:,.0f}\n"
            text += f"  - Risk Margin: ${stats['risk_margin']:,.0f}\n"
            text += f"  - Premium: ${stats['premium']:,.0f}\n\n"

            text += f"• {second_cohort}:\n"
            text += f"  - Expected Loss: ${stats['expected_loss_bad']:,.0f}\n"
            text += f"  - Expenses: ${stats['expenses_bad']:,.0f}\n"
            text += f"  - Premium: ${stats['premium_bad']:,.0f}\n\n"

            premium_diff = stats['premium_bad'] - stats['premium']
            premium_ratio = stats['premium_bad'] / stats['premium']

            text += f"• Premium Difference: ${premium_diff:,.0f} ({premium_ratio:.1f}x)\n\n"
            text += "• Key Formula: Premium = Expected Loss / (1 - Expense - Risk)"

            return text
        else:
            # Original interpretation
            text = "Insurance Premium Comparison:\n"
            text += f"• {first_cohort}:\n"
            text += f"  - Est. Accident Frequency: {good_freq:.1%} (probability per year)\n"
            text += f"  - Est. Average Claim Severity: ${good_severity:,.0f} (average cost when a claim occurs)\n"
            text += f"  - Expected Loss: ${stats['expected_loss']:,.2f} (frequency × severity)\n"
            text += f"  - Expenses: ${stats['expenses']:,.2f} ({expense_ratio:.0%} of premium)\n"
            text += f"  - Risk Margin: ${stats['risk_margin']:,.2f} ({risk_margin_ratio:.0%} of premium)\n"
            text += f"  - Final Premium: ${stats['premium']:,.2f}\n\n"

            text += f"• {second_cohort}:\n"
            text += f"  - Est. Accident Frequency: {bad_freq:.1%} (probability per year)\n"
            text += f"  - Est. Average Claim Severity: ${bad_severity:,.0f} (average cost when a claim occurs)\n"
            text += f"  - Expected Loss: ${stats['expected_loss_bad']:,.2f} (frequency × severity)\n"
            text += f"  - Expenses: ${stats['expenses_bad']:,.2f} ({expense_ratio:.0%} of premium)\n"
            text += f"  - Risk Margin: ${stats['risk_margin_bad']:,.2f} ({risk_margin_ratio:.0%} of premium)\n"
            text += f"  - Final Premium: ${stats['premium_bad']:,.2f}\n\n"

            premium_diff = stats['premium_bad'] - stats['premium']
            premium_ratio = stats['premium_bad'] / stats['premium']

            text += f"• Premium Difference: ${premium_diff:,.2f} ({premium_ratio:.1f}x higher for {second_cohort})\n\n"

            text += "• Key Insights:\n"
            text += f"  1. The premium calculation formula is: Premium = Expected Loss / (1 - Expense Ratio - Risk Margin)\n"
            text += f"  2. Both frequency and severity directly affect the premium - if either doubles, expected loss doubles\n"
            text += f"  3. A driver cohort with {premium_ratio:.1f}x higher risk pays {premium_ratio:.1f}x higher premium\n"
            text += f"  4. The expense and risk margin components are proportionally larger for higher-risk driver cohorts\n"

            return text

    # Ethics Rating Module - Updated for mobile
    @reactive.Calc
    def calculate_ethics_grade():
        # These are the "model answers" based on general insurance standards
        model_answers = {
            'drake_rating': False,  # Not appropriate to use Drake listening as a rating factor
            'kendrick_rating': False,  # Not appropriate to use Kendrick listening as a rating factor
            'age_rating': True,  # Age is a commonly used rating factor
            'vehicle_rating': True,  # Vehicle type is a commonly used rating factor
            'religion_rating': False,  # Religion is not appropriate
            'race_rating': False,  # Race/ethnicity is not appropriate
            'experience_rating': True,  # Years of driving experience is a valid rating factor
            'multiproduct_rating': True,  # Multi-product discount is a common and accepted practice
            'speeding_rating': True,  # Speeding convictions are directly related to driving risk
            'driving_rating': True,  # Driving history is universally used
        }

        # Count correct answers
        correct = 0
        total = len(model_answers)

        # Track incorrect answers
        incorrect = []

        for var, model_answer in model_answers.items():
            user_answer = getattr(input, var)()
            if user_answer == model_answer:
                correct += 1
            else:
                # Format the variable name for displaying
                var_formatted = var.replace('_rating', '').replace('_', ' ').title()
                incorrect.append(var_formatted)

        # Calculate score out of 10
        score = round(correct / total * 10)

        # Generate feedback based on score
        if score >= 9:
            feedback = "Excellent! You have a strong understanding of ethical rating considerations."
        elif score >= 7:
            feedback = "Good work! You understand most key ethical rating principles."
        elif score >= 5:
            feedback = "You're on the right track. Consider how these relate to risk vs. discrimination."
        else:
            feedback = "Review how insurers balance predictive value with social fairness."

        # Add specific feedback if there were incorrect answers
        if incorrect:
            feedback += f" Reconsider: {', '.join(incorrect)}."

        return score, feedback, correct, total

    # Display ethics grade output
    @output
    @render.ui
    @reactive.event(input.grade_ethics)
    def ethics_grade_output():
        score, feedback, correct, total = calculate_ethics_grade()

        # Simplified for mobile
        if is_mobile.get():
            return ui.div(
                {"class": "ethics-grade"},
                ui.h3("Your Score:"),
                ui.span(f"{score}/10"),
                ui.p(f"({correct} out of {total} correct)"),
                ui.div({"class": "ethics-feedback"}, feedback),
                ui.br(),
                ui.p("""
                Key considerations:
                • Statistical correlation with risk
                • Causality vs. correlation
                • Controllability
                • Social acceptability
                • Legality
                """)
            )
        else:
            # Original format
            return ui.div(
                {"class": "ethics-grade"},
                ui.h3("Your Rating Variable Score:"),
                ui.span(f"{score}/10"),
                ui.p(f"You got {correct} out of {total} correct."),
                ui.div({"class": "ethics-feedback"}, feedback),
                ui.br(),
                ui.p("""
                Key considerations for rating variables include:
                • Actuarial justification (statistical correlation with risk)
                • Causality vs. correlation
                • Controllability (can a person change this factor?)
                • Social acceptability and potential for discrimination
                • Legality (some factors are prohibited by law in many jurisdictions)
                """),
                ui.HTML("""
            <p><b>Ethical rating variables</b> (shown in <span style="color: #2ECC71">green</span>) typically have direct causal 
            relationships with risk and are often within the driver's control. These include driving history, 
            speeding convictions, vehicle type, and years of experience.</p>
            """),
                ui.HTML("""
            <p><b>Unethical rating variables</b> (shown in <span style="color: #E74C3C">red</span>) are usually 
            discriminatory, outside a person's control, or lack direct causal links to driving behavior.
            These include race/ethnicity, religion, and music preferences. Regulations prohibit their usage in rating.</p>
            """)
            )


# Create and run the app
app = App(app_ui, server)