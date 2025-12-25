lines = args.input.read_text(encoding="utf-8").splitlines()

echoes = engine.process_lines(
    lines=lines,
    cycle=args.cycle,
    persist=args.persist,
)

for echo in echoes:
    json.dump(echo, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
