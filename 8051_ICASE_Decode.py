# @author DerFetzer
# @category 8051
# @keybinding
# @menupath
# @toolbar import ghidra

try:
    from ghidra.ghidra_builtins import *  # noqa: F403
except:  # noqa: E722
    pass

import ghidra

callLocation = currentLocation

dataStartAddress = getUndefinedDataAfter(callLocation.getAddress()).getAddress()

if dataStartAddress.subtract(callLocation.getAddress()) > 4:
    println(
        "Next undefined data is too far away! Is there really an undefined jump table after the call?"
    )

referenceManager = getCurrentProgram().getReferenceManager()

i = 0

while getShort(dataStartAddress.add(i * 4)) != 0:
    referenceData = createData(
        dataStartAddress.add(i * 4),
        ghidra.program.model.data.Pointer16DataType(),
    )
    referenceManager.addMemoryReference(
        callLocation.getAddress(),
        referenceData.getValue(),
        ghidra.program.model.symbol.RefType.COMPUTED_JUMP,
        ghidra.program.model.symbol.SourceType.USER_DEFINED,
        0,
    )

    createWord(dataStartAddress.add(i * 4 + 2))

    i += 1

referenceData = createData(
    dataStartAddress.add(i * 4 + 2),
    ghidra.program.model.data.Pointer16DataType(),
)
referenceManager.addMemoryReference(
    callLocation.getAddress(),
    referenceData.getValue(),
    ghidra.program.model.symbol.RefType.COMPUTED_JUMP,
    ghidra.program.model.symbol.SourceType.USER_DEFINED,
    0,
)
