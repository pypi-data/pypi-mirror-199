__all__ = ["radial_spoke","balanced_radial_spoke"]

from copy import deepcopy
import typing

from pint import Quantity
import numpy as np

import cmrseq

def balanced_radial_spoke(system_specs: cmrseq.SystemSpec,
                          num_samples: int,
                          kr_max: Quantity,
                          angle: Quantity,
                          adc_duration: Quantity,
                          delay: Quantity = Quantity(0., "ms"),
                          prephaser_duration: Quantity = None) -> cmrseq.Sequence:

    seq = radial_spoke(system_specs=system_specs,num_samples=num_samples,
                       kr_max=kr_max,angle=angle,adc_duration=adc_duration,
                       delay=delay,prephaser_duration=prephaser_duration)

    # Copy prephasers
    rewind_block = deepcopy(seq.get_block("radial_prephaser_0"))

    # Shift to end of readout
    ro_duration = seq.get_block("radial_readout_0").duration
    rewind_block.shift_time(ro_duration + rewind_block.duration)

    rewind_block.name = "radial_prephaser_balance"

    seq += cmrseq.Sequence([rewind_block], system_specs=system_specs)
    return seq


def radial_spoke(system_specs: cmrseq.SystemSpec,
                 num_samples: int,
                 kr_max: Quantity,
                 angle: Quantity,
                 adc_duration: Quantity,
                 delay: Quantity = Quantity(0., "ms"),
                 prephaser_duration: Quantity = None) -> cmrseq.Sequence:

    adc_duration = system_specs.time_to_raster(adc_duration, raster="grad")

    ro_amp = (2 * kr_max / adc_duration / system_specs.gamma).to("mT/m")

    readout_pulse = cmrseq.bausteine.TrapezoidalGradient.from_fdur_amp(
        system_specs=system_specs,
        orientation=np.array([1., 0., 0.]),
        flat_duration=adc_duration,
        amplitude=ro_amp, delay=Quantity(0., "ms"),
        name="radial_readout"
    )

    prephaser_area = readout_pulse.area[0] / 2.
    [_, fastest_prep_ramp, fastest_prep_flatdur] = system_specs.get_shortest_gradient(prephaser_area)

    if prephaser_duration is None:
        prephaser_duration = fastest_prep_flatdur + 2 * fastest_prep_ramp
    else:
        # Check if duration is sufficient for _combined_ prephaser gradients
        if prephaser_duration < np.round(fastest_prep_flatdur + 2 * fastest_prep_ramp, 7):
            raise ValueError("Prephaser duration is to short for combined PE+RO k-space traverse.")

    readout_pulse.shift_time(prephaser_duration + delay)

    prephaser_pulse = cmrseq.bausteine.TrapezoidalGradient.from_dur_area(
        system_specs=system_specs,
        orientation=np.array([-1., 0., 0.]),
        duration=prephaser_duration,
        area=prephaser_area,
        delay=delay, name="radial_prephaser")

    if num_samples > 0:
        adc = cmrseq.bausteine.SymmetricADC(system_specs=system_specs, num_samples=num_samples,
                                            duration=adc_duration,
                                            delay=prephaser_duration + delay + readout_pulse.rise_time)
        seq = cmrseq.Sequence([prephaser_pulse, readout_pulse, adc],
                               system_specs=system_specs)
    else:
        seq = cmrseq.Sequence([prephaser_pulse, readout_pulse],
                               system_specs=system_specs)

    sa = np.sin(angle).m_as('dimensionless')
    ca = np.cos(angle).m_as('dimensionless')
    R = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])

    seq.rotate_gradients(R)

    return seq

