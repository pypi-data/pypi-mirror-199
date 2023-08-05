import statistics

from matplotlib import pyplot

from dk_analyzer.models import Event


class Graph:
    def __init__(self, target_hp_percent: float, target_rp_percent: float) -> None:
        self.target_hp_percent = target_hp_percent
        self.target_rp_percent = target_rp_percent
        self._min_ds_cost = 35
        self._max_hp_percent = 100

    def plot(self, events: list[Event]) -> None:
        hp_list: list[float] = []
        rp_list: list[float] = []
        for event in events:
            if not event.is_cast_by_player():
                continue
            hp_list.append(event.hp_percent())
            rp_list.append(event.rp())

        pyplot.grid(zorder=0)
        pyplot.scatter(
            x=rp_list,
            y=hp_list,
            marker="o",
            zorder=4,
        )
        pyplot.xlabel("RP")
        pyplot.ylabel("HP%")
        self._add_visual_aid()
        self._add_title(hp_list, rp_list)
        pyplot.show()

    def _add_visual_aid(self, thickness: float = 3) -> None:
        pyplot.vlines(
            self.target_rp_percent,
            ymin=0,
            ymax=self._max_hp_percent,
            colors="#FE2A17",
            linewidth=thickness,
            zorder=3,
            label=f"{self.target_rp_percent} RP",
        )
        pyplot.hlines(
            self.target_hp_percent,
            xmin=self._min_ds_cost,
            xmax=self.target_rp_percent,
            colors="#FEBD0D",
            linewidth=thickness,
            zorder=2,
            label=f"{self.target_hp_percent}% HP",
        )
        pyplot.fill_between(
            [self._min_ds_cost, self.target_rp_percent],
            self.target_hp_percent,
            self._max_hp_percent,
            color="black",
            alpha=0.1,
        )

    def _add_title(self, hp_list: list[float], rp_list: list[float]) -> None:
        mean_rp = round(statistics.mean(rp_list))
        mean_hp = round(statistics.mean(hp_list))
        title = f"DS Usage (mean RP: {mean_rp}, mean HP: {mean_hp}%)"
        pyplot.title(title)
