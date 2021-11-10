from mamba import before, description, context, it
from expects import expect, equal

from mowers import MowersController


with description("Mowers Controller") as self:

    with context("controls a mower"):

        with before.each:
            self.mowers_controller = MowersController()

        with context("rotation"):

            with it("can spin left once"):

                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "L\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 W\n"))

            with it("can spin left twice"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "LL\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 S\n"))

            with it("can spin left three times"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "LLL\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 E\n"))

            with it("can spin left four times"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "LLLL\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 N\n"))

            with it("can spin right once"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "R\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 E\n"))

            with it("can spin right twice"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "RR\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 S\n"))

            with it("can spin right three times"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "RRR\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 W\n"))

            with it("can spin right four times"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "RRRR\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 N\n"))

        with context("movement"):

            with it("can move North forward"):
                instructions = "5 5\n" \
                               "0 0 N\n" \
                               "M\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 1 N\n"))

            with it("can move East forward"):
                instructions = "5 5\n" \
                               "0 0 E\n" \
                               "M\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("1 0 E\n"))

            with it("can move South forward"):
                instructions = "5 5\n" \
                               "0 1 S\n" \
                               "M\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 S\n"))

            with it("can move West forward"):
                instructions = "5 5\n" \
                               "1 0 W\n" \
                               "M\n"

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal("0 0 W\n"))

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
