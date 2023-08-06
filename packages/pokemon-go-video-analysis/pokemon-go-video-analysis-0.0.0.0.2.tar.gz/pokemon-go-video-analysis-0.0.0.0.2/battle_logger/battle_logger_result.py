from typing import Dict, List, Optional

import ezplotly as ep
import pandas as pd
from ezplotly import EZPlotlyPlot


class BattleLoggerResult:
    """
    Result of the BattleLoggerOp operation.
    """

    def __init__(self, pokemon_in_frames: Dict[str, List[int]]):
        """
        param pokemon_in_frames: Dictionary mapping Pokémon names to the frames in which they appear.
        """
        self.pokemon_in_frames: Dict[str, List[int]] = pokemon_in_frames

    def plot(
        self,
        outfile: Optional[str] = None,
        suppress_output: bool = False,
    ) -> None:
        """
        Plots the result of the BattleLoggerOp operation.

        param outfile: The path to the output file. If None, the plot is not saved to file.
        param suppress_output: If True, the plot is not displayed.
        """
        keys = list(self.pokemon_in_frames.keys())
        pokemon_names = [key[0] for key in keys]
        pokemon_owner = [key[1] for key in keys]
        whose_pokemon = [
            "Opponent's" if owner == "opponent" else "My" for owner in pokemon_owner
        ]
        h: List[Optional[EZPlotlyPlot]] = [None] * len(pokemon_names)
        for i, hit in enumerate(pokemon_names):
            matched_indices = self.pokemon_in_frames[keys[i]]
            h[i] = ep.scattergl(
                x=matched_indices,
                y=[whose_pokemon[i] + " " + hit] * len(matched_indices),
                xlabel="Video Frame",
                ylabel="Detected Pokemon",
            )
        ep.plot_all(
            h, panels=[1] * len(h), outfile=outfile, suppress_output=suppress_output
        )

    def vis(self):
        """
        Visualizes the result of the BattleLoggerOp operation.
        """
        self.plot(suppress_output=False)

    def to_df(self) -> pd.DataFrame:
        """
        Saves the result of the BattleLoggerOp operation to a CSV file.
        """
        keys = list(self.pokemon_in_frames.keys())
        pokemon_names = [key[0] for key in keys]
        pokemon_owner = [key[1] for key in keys]
        frames = [self.pokemon_in_frames[key] for key in keys]
        df = pd.DataFrame(
            {"Pokemon": pokemon_names, "Owner": pokemon_owner, "Frames": frames}
        )
        return df
