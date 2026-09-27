from manim import *
import numpy as np

class FederatedLearningAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Învățare federată", font_size=42, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create local models
        local_model_1 = self.create_model("Modelul clientului 1", LEFT * 4 + UP * 1, GREEN)
        local_model_2 = self.create_model("Modelul clientului n", RIGHT * 4 + UP * 1, RED)
        
        label_g1 = MathTex("g_1", font_size=24, color=GREEN)
        label_g1.move_to(LEFT * 4 + DOWN * 0.8)
        
        label_g2 = MathTex("g_n", font_size=24, color=RED)
        label_g2.move_to(RIGHT * 4 + DOWN * 0.8)

        # Create global model (initially invisible) - moved up to avoid formula overlap
        global_model = self.create_model("Modelul global", ORIGIN + DOWN * 0.5, YELLOW)
        global_model.set_opacity(0)
        
        # Add models to scene
        self.play(
            FadeIn(local_model_1),
            FadeIn(local_model_2),
            Write(label_g1),
            Write(label_g2)
        )

        dots = MathTex(r"\cdots", font_size=36, color=WHITE)
        dots.move_to(ORIGIN + UP * 1)  # Positioned between the models
        self.play(Write(dots))

        self.wait(1)
        
        # Show local training
        self.show_local_training(local_model_1, local_model_2)
        
        # Show global aggregation
        self.show_global_aggregation(local_model_1, local_model_2, global_model)
        
        # Show final result
        self.show_final_result(local_model_1, local_model_2, global_model)
        
        self.wait(3)
    
    def create_model(self, name, position, color):
        """Create a visual representation of a neural network model"""
        model_group = VGroup()
        
        # Model name
        model_name = Text(name, font_size=20, color=color)  # Reduced font size
        model_name.move_to(position + UP * 1.2)  # Adjusted position
        
        # Neural network visualization - made smaller
        layers = [3, 4, 3, 2]  # Reduced neurons per layer
        network = VGroup()
        
        for i, layer_size in enumerate(layers):
            layer = VGroup()
            for j in range(layer_size):
                # Use hollow circles for parameters - made smaller
                neuron = Circle(radius=0.12, color=color, fill_opacity=0)
                neuron.move_to(position + RIGHT * (i * 1.2 - 1.8) + UP * (j * 0.35 - layer_size * 0.175 + 0.175))
                layer.add(neuron)
            network.add(layer)
        
        # Add connections between layers
        connections = VGroup()
        for i in range(len(layers) - 1):
            for neuron1 in network[i]:
                for neuron2 in network[i + 1]:
                    connection = Line(
                        neuron1.get_center(),
                        neuron2.get_center(),
                        color=color,
                        stroke_width=0.8,
                        stroke_opacity=0.3
                    )
                    connections.add(connection)
        
        model_group.add(model_name, network, connections)
        return model_group
    
    def show_local_training(self, model1, model2):
        """Show local training with SGD formulas"""
        # SGD Formula - positioned at the bottom
        sgd_formula = MathTex(
            r"\mathbf{w}_{t+1}^{k} = \mathbf{w}_{t}^{k} - \eta_{t} \nabla F_{k}(\mathbf{w}_{t}^{k})",
            font_size=28  # Reduced font size
        )
        sgd_formula.to_edge(DOWN)
        sgd_formula.shift(UP * 0.3)
        
        sgd_label = Text("SGD", font_size=20, color=PURPLE)
        sgd_label.next_to(sgd_formula, UP, buff=0.2)
        
        self.play(Write(sgd_label), Write(sgd_formula))
        self.wait(1)
        
        # Animate local training
        for round_num in range(2):
            # Show training iterations
            training_text = Text(f"Runda nr. {round_num + 1}", font_size=18, color=WHITE)
            training_text.to_edge(UP, buff=1.5)
            
            self.play(Write(training_text))
            
            # Animate parameter updates (make neurons pulse)
            for model in [model1, model2]:
                neurons = model[1]  # Get the network part
                animations = []
                for layer in neurons:
                    for neuron in layer:
                        animations.append(neuron.animate.scale(1.3).set_fill(neuron.color, 0.3))
                
                self.play(*animations, run_time=0.5)
                
                # Reset neurons
                reset_animations = []
                for layer in neurons:
                    for neuron in layer:
                        reset_animations.append(neuron.animate.scale(1/1.3).set_fill(neuron.color, 0))
                
                self.play(*reset_animations, run_time=0.5)
            
            self.play(FadeOut(training_text))
        
        self.play(FadeOut(sgd_label), FadeOut(sgd_formula))
    
    def show_global_aggregation(self, model1, model2, global_model):
        """Show global model aggregation"""
        # Averaging formula - positioned at the bottom, below global model
        avg_formula = MathTex(
            r"\mathbf{w}_{t+1} = \sum_{k=1}^N p_k w_t^k",
            font_size=28  # Reduced font size
        )
        avg_formula.to_edge(DOWN)
        avg_formula.shift(UP * 0.3)
        
        avg_label = Text("Procedeul FedAvg", font_size=20, color=PURPLE)
        avg_label.next_to(avg_formula, UP, buff=0.2)
        
        self.play(Write(avg_label), Write(avg_formula))
        self.wait(1)
        
        # Show parameter transfer with individual arrows
        arrows1 = []
        arrows2 = []
        
        # Create arrows from local models to global model
        for i in range(3):  # 3 arrows from each model
            arrow1 = Arrow(
                model1.get_center() + DOWN * 0.3,
                global_model.get_center() + UP * 0.3 + LEFT * (i - 1) * 0.25,
                color=GREEN,
                stroke_width=2
            )
            arrow2 = Arrow(
                model2.get_center() + DOWN * 0.3,
                global_model.get_center() + UP * 0.3 + RIGHT * (i - 1) * 0.25,
                color=RED,
                stroke_width=2
            )
            arrows1.append(arrow1)
            arrows2.append(arrow2)
        
        # Animate parameter transfer - create animations for individual arrows
        arrow_animations = []
        for arrow in arrows1 + arrows2:
            arrow_animations.append(GrowArrow(arrow))
        
        self.play(*arrow_animations)
        self.wait(1)
        
        # Fade in global model
        self.play(global_model.animate.set_opacity(1))
        self.wait(1)
        
        # Remove arrows
        fade_animations = []
        for arrow in arrows1 + arrows2:
            fade_animations.append(FadeOut(arrow))
        
        self.play(*fade_animations)
        self.play(FadeOut(avg_label), FadeOut(avg_formula))
    
    def show_final_result(self, model1, model2, global_model):
        """Show the final federated learning result"""
        # Fade local models
        self.play(
            model1.animate.set_opacity(0.3),
            model2.animate.set_opacity(0.3)
        )
        
        # Highlight global model
        global_neurons = global_model[1]  # Get the network part
        highlight_animations = []
        
        for layer in global_neurons:
            for neuron in layer:
                highlight_animations.append(
                    neuron.animate.set_stroke(PURPLE, width=3)
                )
        
        self.play(*highlight_animations)
        
        # Final formula - positioned well below the global model
        final_formula = MathTex(
            r"g = G(g_1, g_2, \ldots, g_n)",
            font_size=26,  # Reduced font size
            color=YELLOW
        )
        final_formula.to_edge(DOWN)
        final_formula.shift(UP * 0.8)  # More space from bottom
        
        final_label = Text("Algoritm încheiat", font_size=20, color=YELLOW)
        final_label.next_to(final_formula, UP, buff=0.2)
        
        self.play(Write(final_label), Write(final_formula))
        
        # Add convergence text - positioned even lower
        convergence_text = Text(
            "Modelul global final",
            font_size=16,  # Smaller font
            color=GREEN
        )
        convergence_text.to_edge(DOWN)
        convergence_text.shift(UP * 0.2)
        
        self.play(Write(convergence_text))
        
        # Final highlight animation
        self.play(
            global_model.animate.scale(1.1),
            run_time=1
        )
        self.play(
            global_model.animate.scale(1/1.1),
            run_time=1
        )

if __name__ == "__main__":
    # Pentru a randa animația, rulează:
    # manim -pql main.py FederatedLearningAnimation
    pass