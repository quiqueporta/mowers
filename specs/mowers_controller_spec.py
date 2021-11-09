from mamba import before, description, context, it
from expects import expect, equal

from mowers import MowersController


with description("Mowers Controller") as self:

    with it("controls one mower"):

        mowers_controller = MowersController()

        instructions = "5 5\n" \
                       "1 2 N\n" \
                       "LMLMLMLMM\n"

        result = mowers_controller.execute(instructions)

        expect(result).to(equal("1 3 N\n"))

    with it("controls more than one mower"):

        mowers_controller = MowersController()

        instructions = "5 5\n" \
                       "1 2 N\n" \
                       "LMLMLMLMM\n" \
                       "3 3 E\n" \
                       "MMRMMRMRRM\n"

        result = mowers_controller.execute(instructions)

        expected_result = "1 3 N\n" \
                          "5 1 E\n"
        expect(result).to(equal(expected_result))
