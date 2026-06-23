"""Main CLI application orchestrator."""

from typing import Any

from iris_classifier.cli.interpreter import CommandInterpreter
from iris_classifier.cli.menu import MenuBuilder
from iris_classifier.cli.responses import ResponseManager
from iris_classifier.core.session import ExperimentSession
from iris_classifier.data.schema import IrisSample
from iris_classifier.logger import get_logger


class IrisClassifierApp:
    """Main CLI application for Iris classification."""

    def __init__(self) -> None:
        """Initialize application."""
        self.session = ExperimentSession()
        self.logger = get_logger()
        self.running = True
        self.command_mode = False
        self.interpreter = CommandInterpreter()
        self.responses = ResponseManager()

    def _print_header(self) -> None:
        """Print application header."""
        print("\n" + "=" * 60)
        print("  🌸 IRIS FLOWER CLASSIFICATION SYSTEM 🌸")
        print("  Supervised Learning with K-Nearest Neighbors")
        print("=" * 60)
        print(self.responses.format("welcome"))

    def _show_main_menu(self) -> None:
        """Display and handle main menu."""
        menu = (
            MenuBuilder("MAIN MENU")
            .with_option("1", "Load Dataset", self._menu_load_data)
            .with_option("2", "Preprocess Data", self._menu_preprocess)
            .with_option("3", "Train Model", self._menu_train)
            .with_option("4", "Evaluate Model", self._menu_evaluate)
            .with_option("5", "Predict New Sample", self._menu_predict)
            .with_option("6", "Tune K Value", self._menu_tune_k)
            .with_option("7", "View Session Info", self._menu_session_info)
            .with_option("8", "Quick Demo (Auto)", self._menu_quick_demo)
            .with_option("9", "Reset Session", self._menu_reset)
            .with_option("0", "Exit", self._menu_exit)
            .build()
        )
        menu.run()

    def _menu_load_data(self) -> None:
        """Load dataset."""
        print("\n⏳ " + self.responses.format("load_start"))
        self.session.load_data()
        print("✓ " + self.responses.format("load_success"))
        print(self.session.dataset.summary())

    def _menu_preprocess(self) -> None:
        """Preprocess data."""
        if not self.session.is_data_loaded:
            print("❌ " + self.responses.format("invalid_input"))
            return

        print("\n⏳ " + self.responses.format("preprocess_start"))
        self.session.preprocess()
        print("✓ " + self.responses.format("preprocess_success"))
        print(self.session.preprocessed_data.summary())

    def _menu_train(self) -> None:
        """Train model."""
        if not self.session.is_preprocessed:
            print("❌ " + self.responses.format("invalid_input"))
            return

        print("\n" + "=" * 50)
        print("TRAIN MODEL")
        print("=" * 50)

        algorithm = input("Select algorithm (knn/logistic/tree) [default: knn]: ").strip().lower() or "knn"

        k = None
        if algorithm == "knn":
            try:
                k = int(input("Enter K value [default: 3]: ").strip() or 3)
            except ValueError:
                print("❌ " + self.responses.format("invalid_input"))
                return

        print(f"\n⏳ {self.responses.format('train_start')}")
        try:
            self.session.train(k, algorithm)
            print("✓ " + self.responses.format("train_success"))
            print(self.session.trained_model.summary())
        except Exception as e:
            print(f"❌ Training error: {e}")

    def _menu_evaluate(self) -> None:
        """Evaluate model."""
        if not self.session.is_model_trained:
            print("❌ " + self.responses.format("invalid_input"))
            return

        print("\n⏳ " + self.responses.format("evaluate_start"))
        self.session.evaluate()
        print("✓ " + self.responses.format("evaluate_success"))
        print(self.session.evaluation_result.summary())

    def _menu_predict(self) -> None:
        """Predict new sample."""
        if not self.session.is_model_trained:
            print("❌ " + self.responses.format("invalid_input"))
            return

        print("\n" + "=" * 50)
        print("PREDICT NEW SAMPLE")
        print("=" * 50)
        print(self.responses.format("predict_prompt"))

        try:
            sepal_length = float(input("Sepal length (cm): "))
            sepal_width = float(input("Sepal width (cm): "))
            petal_length = float(input("Petal length (cm): "))
            petal_width = float(input("Petal width (cm): "))

            sample = IrisSample(sepal_length, sepal_width, petal_length, petal_width)
            predicted_species = self.session.predict_new_sample(sample)

            print(f"\n✓ {self.responses.format('predict_success')}")
            print(f"  Predicted Species: 🌸 {predicted_species.upper()}")
        except ValueError:
            print("❌ " + self.responses.format("invalid_input"))
        except Exception as e:
            print(f"❌ Prediction error: {e}")

    def _menu_tune_k(self) -> None:
        """Tune K value."""
        if not self.session.is_preprocessed:
            print("❌ " + self.responses.format("invalid_input"))
            return

        print("\n⏳ " + self.responses.format("tune_start"))
        try:
            self.session.tune_k()
            print("✓ " + self.responses.format("tune_success"))
            print(self.session.tuning_result.summary())
        except Exception as e:
            print(f"❌ Tuning error: {e}")

    def _menu_session_info(self) -> None:
        """Display session information."""
        print("\n" + "=" * 50)
        print("SESSION INFORMATION")
        print("=" * 50)

        status = []
        status.append(f"Data Loaded: {'✓' if self.session.is_data_loaded else '✗'}")
        status.append(f"Data Preprocessed: {'✓' if self.session.is_preprocessed else '✗'}")
        status.append(f"Model Trained: {'✓' if self.session.is_model_trained else '✗'}")
        status.append(f"Model Evaluated: {'✓' if self.session.is_evaluated else '✗'}")

        for line in status:
            print(f"  {line}")

        if self.session.command_history:
            print(f"\nCommand History ({len(self.session.command_history)} commands):")
            for i, cmd in enumerate(self.session.get_history(10), 1):
                print(f"  {i}. {cmd}")

    def _menu_quick_demo(self) -> None:
        """Run automated demo."""
        print("\n" + "=" * 50)
        print("QUICK DEMO - AUTOMATED WORKFLOW")
        print("=" * 50)

        try:
            print("\n1️⃣ Loading data...")
            self.session.load_data()
            print("   ✓ Loaded")

            print("\n2️⃣ Preprocessing data...")
            self.session.preprocess()
            print("   ✓ Preprocessed")

            print("\n3️⃣ Training KNN model...")
            self.session.train(k=3, algorithm="knn")
            print("   ✓ Trained")

            print("\n4️⃣ Evaluating model...")
            self.session.evaluate()
            print("   ✓ Evaluated")

            print("\n5️⃣ Making prediction...")
            sample = IrisSample(5.1, 3.5, 1.4, 0.2)
            species = self.session.predict_new_sample(sample)
            print(f"   ✓ Sample {sample} → {species}")

            print("\n✅ Demo complete! Full workflow executed.")
            print(self.session.evaluation_result.summary())
        except Exception as e:
            print(f"❌ Demo error: {e}")

    def _menu_reset(self) -> None:
        """Reset session."""
        confirm = input("\nReset all session data? (y/n): ").lower().strip()
        if confirm == "y":
            self.session.reset()
            print("✓ Session reset")

    def _menu_exit(self) -> None:
        """Exit application."""
        print("\n" + self.responses.format("goodbye"))
        self.running = False

    def _run_command_mode(self) -> None:
        """Run conversational command mode."""
        print("\n" + self.responses.format("command_mode_header"))
        while self.command_mode:
            raw_command = input("cmd> ").strip()
            if not raw_command:
                continue

            self.session.log_command(raw_command)
            action, params = self.interpreter.parse(raw_command)
            if action in {"exit", "back"}:
                print(self.responses.format("exit_command_mode"))
                self.command_mode = False
                break

            self._execute_action(action, params)

    def _execute_action(self, action: str, params: dict[str, Any]) -> None:
        """Execute parsed command action."""
        try:
            if action == "load_data":
                self._menu_load_data()
            elif action == "preprocess":
                self._menu_preprocess()
            elif action == "train":
                self.session.train(params.get("k"), params.get("algorithm", "knn"))
                print("✓ " + self.responses.format("train_success"))
                print(self.session.trained_model.summary())
            elif action == "evaluate":
                self._menu_evaluate()
            elif action == "predict":
                values = params.get("values", [])
                if len(values) == 4:
                    sample = IrisSample(*values)
                    predicted_species = self.session.predict_new_sample(sample)
                    print(f"✓ {self.responses.format('predict_success')}")
                    print(f"  Predicted Species: 🌸 {predicted_species.upper()}")
                else:
                    print(self.responses.format("invalid_input"))
            elif action == "tune_k":
                self._menu_tune_k()
            elif action == "session_info":
                self._menu_session_info()
            elif action == "history":
                self._menu_session_info()
            elif action == "reset":
                self._menu_reset()
            elif action == "help":
                topic = params.get("topic")
                if topic:
                    print(self.interpreter.help_text(topic))
                else:
                    print(self.responses.format("help_text"))
            elif action == "set_mode":
                mode = params.get("mode")
                if mode:
                    try:
                        self.responses.set_mode(mode)
                        print(self.responses.format("mode_changed", mode=self.responses.get_mode()))
                    except ValueError as error:
                        print(f"❌ {error}")
                else:
                    print(self.responses.format("current_mode", mode=self.responses.get_mode()))
            elif action == "unknown":
                print(self.responses.format("unknown_command"))
            else:
                print(self.responses.format("unknown_command"))
        except Exception as e:
            print(f"❌ {e}")

    def run(self) -> None:
        """Run main application."""
        self._print_header()
        print("\n🚀 Type your choice and press Enter to navigate. Type 'help' at any time in command mode.")

        while self.running:
            print("\n1) Main menu")
            print("2) Command mode")
            print("0) Exit")

            choice = input("Enter choice: ").strip().lower()
            if choice == "1":
                self._show_main_menu()
            elif choice == "2":
                self.command_mode = True
                self._run_command_mode()
            elif choice == "0":
                self._menu_exit()
            else:
                print(self.responses.format("unknown_command"))
