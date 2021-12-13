'''Different styles of loading bars for the terminal/console.
*your terminal/console MUST support ANSI escape sequences'''
from re import findall
from math import floor

TBPRESET_LEGACY = [
    "progress [%(l)] %(p) | %(c)/%(m)",
    {
        "%round" : 0,
        "%formt" : -1,
        "lbunit" : 40,
        "lbempt" : "-",
        "lbfill" : "=",
        "spinun" : -1,
        "spinst" : -1
    }
]
TBPRESET_CLASSIC = [
    "\033[33m%(l)\033[0m | (%(c)/%(m), %(p)) | %(s)",
    {
        "%round" : 1,
        "%formt" : -1,
        "lbunit" : 20,
        "lbempt" : ".",
        "lbfill" : "#",
        "spinun" : -1,
        "spinst" : -1
    }
]
TBPRESET_MODERN = [
    " \033[96m%(l)\033[0m | '%(msg)\t' | %(c)/%(m)",
    {
        "%round" : -1,
        "%formt" : -1,
        "lbunit" : 30,
        "lbempt" : "░",
        "lbfill" : "█",
        "spinun" : -1,
        "spinst" : -1
    }
]

class TerminalBar:
    '''Main terminal loading bar class.
    Bar formatting (default = [%(c)/%(m) (%(p))]):
    - use %(____) around certain chars to format.
    c:    current value
    m:    max value
    p:    percentage
    l:    loading bar
    s:    spinner
    msg:  custom message
    default value: [CURRENT/MAX (PERCENT)], e.g. [192/1000, (19.20%)]
    '''
    def __init__(self, max_value: int, cur_value: int = 0, bar_format: str = "[%(c)/%(m) (%(p))]", init_line: bool = True):
        self.bar_state = [cur_value, max_value]
        self.bar_format = bar_format
        self.confg = {
            "%round" : 2,
            "%formt" : "#%",
            "lbunit" : 10,
            "lbempt" : " ",
            "lbfill" : "|",
            "spinun" : max_value / 50,
            "spinst" : "-\\|/-\\|/",
        }
        if init_line:
            print()

    def update_preset(self, preset) -> None:
        '''Set style of a bar to a preset,
        Included are (TBPRESET_): LEGACY, CLASSIC'''
        if preset[0]:
            self.bar_format = preset[0]
        self.update_confg(preset[1])

    def update_value(self, new_cur: int) -> None:
        '''Updates current value of bar'''
        self.bar_state[0] = new_cur

    def update_confg(self, new_confg: list) -> None:
        '''Set a new configuration, each value in the list represents a setting:
        - %round: number of decimal places to round percentages to (2:int)
        - %formt: format of percentages
        - lbunit: number of units on a loading bar (10:int)
        - lbempt: character to represent unfilled units of loading bar (' ':str)
        - lbfill: character to represent filled units of loading bar ('|':str)
        - spinun: on every xth of the bar being filled, rotate the spinner ((max_value/50):float)
        - spinst: the stages of the spinner ("-\\|/-\\|/":str or list[str])
        * Use a value of -1 to keep the old value
        '''
        self.confg = {
            val : self.confg[val] if new_confg[val] == -1 else new_confg[val]
            for i, val in enumerate(new_confg)
        }

    def get_percentage(self) -> str:
        '''Returns percentage of bar as formatted string'''
        percent = self.bar_state[0] / self.bar_state[1] * 100.0
        return self.confg['%formt'].replace("#", str(round(percent, self.confg['%round'])))

    def get_spinner(self) -> str:
        '''Returns a spinner state for spinning element'''
        spin_index = self.bar_state[0] / self.confg['spinun'] % len(self.confg['spinst'])
        return self.confg['spinst'][floor(min(spin_index, len(self.confg['spinst']) - 1))]

    def get_loading_bar(self) -> str:
        '''Returns visual loading bar that is <units> wide'''
        n_filled = round(self.bar_state[0] / self.bar_state[1] * self.confg['lbunit'])
        return (self.confg['lbfill'] * n_filled)\
               + (self.confg['lbempt'] * (self.confg['lbunit'] - n_filled))

    def get_bar(self, message: str = "Loading...") -> str:
        '''Returns formatted bar'''
        final = self.bar_format
        for found in findall(r'%\([^)]*\)', self.bar_format):
            match found[2:-1]:
                case 'c':
                    final = final.replace("%(c)", str(self.bar_state[0]))
                case 'm':
                    final = final.replace("%(m)", str(self.bar_state[1]))
                case 'p':
                    final = final.replace("%(p)", self.get_percentage())
                case 'l':
                    final = final.replace("%(l)", self.get_loading_bar())
                case 's':
                    final = final.replace("%(s)", self.get_spinner())
                case 'msg':
                    final = final.replace("%(msg)", message)
        return final

    def render(self, cursor_cmd: str = "\033[1F", message: str = "Loading...") -> None:
        '''Renders the bar to the screen,
        change the <cursor_cmd> to change how it renders
        see: https://en.wikipedia.org/wiki/ANSI_escape_code#CSI'''
        print(f"{cursor_cmd}{self.get_bar(message)}")

    def update(self, new_val, message: str = "Loading...") -> None:
        '''Full update and render.'''
        self.update_value(new_val)
        self.render(message = message)

class CompoundTerminalBar:
    '''Class for multiple TerminalBars'''
    def __init__(self):
        self.bars = []
        self.bar_msgs = []
        self.disappear_on_fill = False

    def add_bar(self, maxval: int, message: str):
        '''Add a bar'''
        self.bars.append(TerminalBar(maxval, init_line = False))
        self.bar_msgs.append(message)

    def set_preset(self, preset: list):
        '''Set a preset'''
        for cbar in self.bars:
            cbar.update_preset(preset)

    def update(self, newvals: list[int]):
        '''Update and render bars'''
        rendered = 0
        for i, cbar in enumerate(self.bars):
            if self.disappear_on_fill and cbar.bar_state[0] >= cbar.bar_state[1]:
                print("\033[K")
                rendered += 1
                continue
            if len(newvals) > i:
                if newvals[i] != -1:
                    cbar.update_value(newvals[i])
            cbar.render("", self.bar_msgs[i])
            rendered += 1
        print(f"\033[{rendered}F", end = "")


# Usage example
if __name__ == "__main__":
    ctb = CompoundTerminalBar()
    ctb.add_bar(20000, "First bar")
    ctb.add_bar(10000, "Second bar")
    ctb.add_bar(30000, "Third bar")
    ctb.disappear_on_fill = True
    ctb.set_preset(TBPRESET_MODERN)

    for i in range(20001):
        ctb.update([i, -1, -1])
    for i in range(10001):
        ctb.update([-1, i, -1])
    for i in range(30001):
        ctb.update([-1, -1, i])
