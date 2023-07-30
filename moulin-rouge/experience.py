from math import pow
from attrs import define

@define
class Experience:
    tnl: int = 100
    factor: float = 0.95
    levels: int = 20
    _total: int = 0
    _level: int = 0

    def experience_table(self):
        print("{0:10}|  {1:>13}|  {2:>13}|".format("Level", "Exp acquired", "Next level"))
        while self._level < self.levels:
            print(f"Level {self._level :2}  |  {int(self._total) : >12} |  {int(self.tnl) : >12} |")
            self._total += self.tnl
            self.tnl = self.tnl * (1 + pow(self.factor,self._level))
            self._level += 1


