from mamba import description, context, it
from expects import expect, be_true, be_false

from mowers import test


with description("Mowers"):

    with it("works"):
        expect(test()).to(be_true)
