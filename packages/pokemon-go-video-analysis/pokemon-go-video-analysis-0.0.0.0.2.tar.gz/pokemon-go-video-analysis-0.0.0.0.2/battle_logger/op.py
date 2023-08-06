import os
from typing import Optional

import numpy as np
import pandas as pd
from algo_ops.ops.op import Op
from ocr_ops.framework.op.result.ocr_result import OCRPipelineResult

from battle_logger.battle_logger_result import BattleLoggerResult


class BattleLoggerOp(Op):
    def __init__(self):
        """
        Operation that parses the battle log and determines which Pokémon are in the battle.
        """
        super().__init__(func=self.parse_battle_log)
        self.input: Optional[OCRPipelineResult] = None
        self.output: Optional[BattleLoggerResult] = None

    @staticmethod
    def parse_battle_log(ocr_result: OCRPipelineResult) -> BattleLoggerResult:
        # obtain the OCR result as a dataframe of detected text boxes
        df = ocr_result.to_df()
        df["frame"] = [
            int(os.path.basename(f).split(".")[0][3:]) for f in df.input_path
        ]

        # load Pokémon moves file
        pokemon_df = pd.read_csv(os.path.join("..", "pkmn_data", "pokemon_moves.csv"))
        available_pokemon = pokemon_df["Pokémon"].str.lower().values

        # determine which Pokémon are in the battle
        found = df.text.str.contains("|".join(available_pokemon))
        found[found.isnull()] = False
        df["found_pokemon"] = df.text.str.lower().str.extract(
            "(" + "|".join(available_pokemon) + ")", expand=False
        )
        pokemon_in_battle = df.found_pokemon.unique().tolist()
        pokemon_in_battle.remove(np.nan)

        # determine whose pokemon based on screen location
        opponent_loc = np.array([696, 164], dtype=float)
        distance_t = 10
        pokemon_owner = list()
        for hit in pokemon_in_battle:
            polygon_texts = df.bounding_box[df.found_pokemon == hit].values.astype(str)
            starting_vertices = [
                text[str(text).find("(") + 2 : str(text).find(",")]
                for text in polygon_texts
            ]
            starting_vertices = np.array(
                [[int(v.split()[0]), int(v.split()[1])] for v in starting_vertices],
                dtype=float,
            )
            d = np.sum(np.abs(starting_vertices - opponent_loc), 1)
            if any(d <= distance_t):
                pokemon_owner.append("opponent")
            else:
                pokemon_owner.append("you")

        # determine mapping to frame number
        pokemon_in_frames = {
            (pokemon, pokemon_owner[i]): df.frame[df.found_pokemon == pokemon]
            .unique()
            .tolist()
            for i, pokemon in enumerate(pokemon_in_battle)
        }
        return BattleLoggerResult(pokemon_in_frames=pokemon_in_frames)

    def vis(self) -> None:
        """
        Visualizes the result of the BattleLoggerOp operation.
        """
        if self.output is None:
            raise ValueError("Output is None. Run the operation first.")
        self.output.vis()

    def vis_input(self) -> None:
        """
        Visualizes the input to the BattleLoggerOp operation.
        """
        if self.input is None:
            raise ValueError("Input is None. Run the operation first.")
        print(self.input.to_df())

    def save_input(self, out_path: str, basename: Optional[str] = None) -> None:
        """
        Saves the input to the BattleLoggerOp operation.
        """
        if self.input is None:
            raise ValueError("Input is None. Run the operation first.")
        self.input.to_df().to_csv(
            os.path.join(out_path, basename + ".csv"), index=False
        )

    def save_output(self, out_path, basename: Optional[str] = None) -> None:
        """
        Saves the output of the BattleLoggerOp operation.
        """
        if self.output is None:
            raise ValueError("Output is None. Run the operation first.")
        self.output.to_df().to_csv(
            os.path.join(out_path, basename + ".csv"), index=False
        )
        self.output.plot(
            outfile=os.path.join(out_path, basename + ".png"), suppress_output=True
        )
