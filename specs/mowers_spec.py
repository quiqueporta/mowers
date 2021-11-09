from mamba import before, description, context, it
from expects import expect, equal

from mowers import Mower


with description("Mower") as self:

    with context("rotation"):

        with before.each:
            self.mower = Mower()

        with it("can spin left once"):
            result = self.mower.execute("L")

            expect(result).to(equal("0 0 W"))

        with it("can spin left twice"):
            result = self.mower.execute("LL")

            expect(result).to(equal("0 0 S"))

        with it("can spin left three times"):
            result = self.mower.execute("LLL")

            expect(result).to(equal("0 0 E"))

        with it("can spin left four times"):
            result = self.mower.execute("LLLL")

            expect(result).to(equal("0 0 N"))

        with it("can spin right once"):
            result = self.mower.execute("R")

            expect(result).to(equal("0 0 E"))

        with it("can spin right twice"):
            result = self.mower.execute("RR")

            expect(result).to(equal("0 0 S"))

        with it("can spin right three times"):
            result = self.mower.execute("RRR")

            expect(result).to(equal("0 0 W"))

        with it("can spin right four times"):
            result = self.mower.execute("RRRR")

            expect(result).to(equal("0 0 N"))
