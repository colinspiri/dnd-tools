import initiative as init
import parser

# Get initiative order
initiative = init.input_initiative()
initiative.show_order()

# Cycle through order
initiative.show_round()
while True:
    print()

    initiative.show_turn()

    parser.get_input(initiative)
