from shiny import reactive, render, ui
import random
import numpy as np
import matplotlib.pyplot as plt
from modules.risk_pooling import demonstrate_risk_pooling
from modules.driver_comparison import demonstrate_driver_comparison
from modules.premium_calculation import demonstrate_premium_calculation
from modules.ethics import grade_ethics_answers


def create_server_function():
    """Creates and returns the server function for the Shiny app"""

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

        # Ethics of Rating Module
        @reactive.Calc
        def ethics_answers():
            """Collects all the ethics module answers"""
            return {
                'drake_rating': input.drake_rating(),
                'kendrick_rating': input.kendrick_rating(),
                'age_rating': input.age_rating(),
                'vehicle_rating': input.vehicle_rating(),
                'religion_rating': input.religion_rating(),
                'race_rating': input.race_rating(),
                'experience_rating': input.experience_rating(),
                'multiproduct_rating': input.multiproduct_rating(),
                'speeding_rating': input.speeding_rating(),
                'driving_rating': input.driving_rating()
            }

        @output
        @render.ui
        @reactive.event(input.grade_ethics)
        def ethics_grade_output():
            grade_results = grade_ethics_answers(ethics_answers())
            score = grade_results['score']
            feedback = grade_results['feedback']
            correct = grade_results['correct']
            total = grade_results['total']

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

    return server