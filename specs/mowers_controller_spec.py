from mamba import before, description, context, it
from expects import expect, equal

from mowers import MowersController


with description("Mowers Controller") as self:

    with context("controls a mower"):

        with before.each:
            self.mowers_controller = MowersController()

        with context("rotation"):

            with it("can spin left once"):

                instructions = ["5 5", "0 0 N", "L"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 W"]))

            with it("can spin left twice"):
                instructions = ["5 5", "0 0 N", "LL"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 S"]))

            with it("can spin left three times"):
                instructions = ["5 5", "0 0 N", "LLL"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 E"]))

            with it("can spin left four times"):
                instructions = ["5 5", "0 0 N", "LLLL"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 N"]))

            with it("can spin right once"):
                instructions = ["5 5", "0 0 N", "R"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 E"]))

            with it("can spin right twice"):
                instructions = ["5 5", "0 0 N", "RR"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 S"]))

            with it("can spin right three times"):
                instructions = ["5 5", "0 0 N", "RRR"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 W"]))

            with it("can spin right four times"):
                instructions = ["5 5", "0 0 N", "RRRR"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 N"]))

        with context("movement"):

            with it("can move North forward"):
                instructions = ["5 5", "0 0 N", "M"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 1 N"]))

            with it("can move East forward"):
                instructions = ["5 5", "0 0 E", "M"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["1 0 E"]))

            with it("can move South forward"):
                instructions = ["5 5", "0 1 S", "M"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 S"]))

            with it("can move West forward"):
                instructions = ["5 5", "1 0 W", "M"]

                result = self.mowers_controller.execute(instructions)

                expect(result).to(equal(["0 0 W"]))

    with it("controls more than one mower"):

        mowers_controller = MowersController()

        instructions = ["5 5", "1 2 N", "LMLMLMLMM", "3 3 E", "MMRMMRMRRM"]

        result = mowers_controller.execute(instructions)

        expected_result = ["1 3 N", "5 1 E"]
        expect(result).to(equal(expected_result))
