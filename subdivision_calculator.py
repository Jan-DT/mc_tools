# Minecraft Subdivision Calculator by 4FA
#
# This script calculates the intervals between two positions in Minecraft,
# given the number of posts and the width of the posts.

# Changes the length of the visual representation of the subdivision
MAX_VISUAL_LENGTH = 100


class Subdivision1D:
    def __init__(self, pos_a: int, pos_b: int, post_width: int = 1):
        self.pos_a = pos_a
        self.pos_b = pos_b
        if post_width < 1: raise ValueError("The post width must be at least 1")
        self.post_width = post_width

    @staticmethod
    def calculate_distance(pos_a: int, pos_b: int) -> float:
        return abs(pos_a - pos_b) + 1

    def distance(self) -> float:
        return self.calculate_distance(self.pos_a, self.pos_b)

    @staticmethod
    def calculate_post_width(posts: int, post_width: int) -> int:
        """Calculates the total width of the posts in the subdivision."""
        if post_width < 1 or posts < 1:
            raise ValueError("The post width and the number of posts must be at least 1")
        return posts * post_width

    @staticmethod
    def calculate_intervals(pos_a: int, pos_b: int, posts: int, post_width: int = 1) -> float:
        if post_width < 1: raise ValueError("The post width must be at least 1")
        if Subdivision1D.calculate_post_width(posts, post_width) > Subdivision1D.calculate_distance(pos_a, pos_b):
            raise ValueError("The total size of the posts must be less than the distance between the two positions")
        if 2 > posts > abs(pos_a - pos_b):
            raise ValueError("The number of posts must be more than 2 and less than the total distance")
        return ((Subdivision1D.calculate_distance(pos_a, pos_b) - Subdivision1D.calculate_post_width(posts, post_width))
                / (posts - 1))

    def calculate(self) -> list:
        """Calculates the valid (full block) intervals between the two positions."""
        _valid_intervals = []
        for _posts in range(2, abs(self.pos_a - self.pos_b) + 1):
            try:
                _interval = self.calculate_intervals(self.pos_a, self.pos_b, _posts, self.post_width)
                if _interval.is_integer() and _interval > 0:
                    _valid_intervals.append((_posts, _interval))
            except ValueError:
                pass
        return _valid_intervals


def visualize_subdivision(posts: int, post_width: int, interval: int):
    """Visualizes the subdivision with posts and gaps."""
    _visual = ""
    _length = posts * post_width + (posts - 1) * interval
    for _i in range(posts):
        _visual += "⌧" * post_width + ("·" * interval if _i < posts - 1 else "")
        if len(_visual) > MAX_VISUAL_LENGTH:
            return _visual[:MAX_VISUAL_LENGTH] + "..."
    return _visual[:_length]


def run():
    print("\n┌" + "─" * 41 + "┐")
    print(f"│ Minecraft Subdivision Calculator by 4FA │")
    print("└" + "─" * 41 + "┘\n")

    try:
        uinput: list[str] = input("Enter the start and end coordinates, and width of the posts, like 20 50 2.\n"
                                  "You can also calculate multiple post widths, like 20 50 1 2 3\n> ").split(' ')
        if len(uinput) < 2: raise ValueError("Not enough arguments given")
        pos_a, pos_b = int(uinput.pop(0)), int(uinput.pop(0))
        post_widths: list[int] = list(map(int, uinput)) or [1]

        print(f"Calculating the intervals between {pos_a} and {pos_b} ({Subdivision1D.calculate_distance(pos_a, pos_b)} blocks)" + (
                f" with a post width of {post_widths[0]}..." if len(post_widths) <= 1 else
                f" with post widths: {', '.join(map(str, post_widths))}..."))

        for post_width in post_widths:
            sub = Subdivision1D(pos_a, pos_b, post_width)
            intervals = sub.calculate()
            if intervals:
                print(f"Found {len(intervals)} solutions for post width {post_width}:")
                for posts, interval in intervals:
                    msg = f"* Posts: {posts} - Gaps: {posts - 1} - Blocks between: {int(interval)}"
                    print(msg + max(3, 50 - len(msg)) * " " + visualize_subdivision(posts, post_width, int(interval)))
            else:
                print(f"No solutions found for post width {post_width}...")

    except ValueError as e:
        print(f"Invalid situation: {e}")


if __name__ == "__main__":
    while True:
        run()
        if input("\nPress 'enter' to continue, or type 'quit' to quit.").lower() in ("quit", "exit", "q"): break
