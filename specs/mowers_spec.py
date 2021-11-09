from mamba import description, context, it
from expects import expect, be_true, be_false, equal

from mowers import Mower


with description("Mower"):

    with it("can rorate left once"):
        mower = Mower()

        result = mower.execute("L")

        expect(result).to(equal("0 0 W"))

    with it("can rorate left twice"):
        mower = Mower()

        result = mower.execute("LL")

        expect(result).to(equal("0 0 S"))

    with it("can rorate left three times"):
        mower = Mower()

        result = mower.execute("LLL")

        expect(result).to(equal("0 0 E"))

    with it("can rorate left four times"):
        mower = Mower()

        result = mower.execute("LLLL")

        expect(result).to(equal("0 0 N"))

    with it("can rotate right once"):
        mower = Mower()

        result = mower.execute("R")

        expect(result).to(equal("0 0 E"))

    with it("can rotate right twice"):
        mower = Mower()

        result = mower.execute("RR")

        expect(result).to(equal("0 0 S"))

    with it("can rotate right three times"):
        mower = Mower()

        result = mower.execute("RRR")

        expect(result).to(equal("0 0 W"))

    with it("can rotate right four times"):
        mower = Mower()

        result = mower.execute("RRRR")

        expect(result).to(equal("0 0 N"))
