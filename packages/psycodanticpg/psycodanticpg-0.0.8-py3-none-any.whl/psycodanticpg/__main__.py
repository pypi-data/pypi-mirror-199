if __name__ == "__main__":
    import os
    import sys

    script_path = os.path.abspath(__file__)
    arguments = sys.argv[1:]
    for argument in arguments:
        script_path = os.path.join(
            os.path.dirname(script_path), "scripts", f"{argument}.py"
        )
        if os.path.isfile(script_path):
            script_module = __import__(
                f"psycodanticpg.scripts.{argument}", fromlist=["run"]
            )
            script_module.run()
            break
