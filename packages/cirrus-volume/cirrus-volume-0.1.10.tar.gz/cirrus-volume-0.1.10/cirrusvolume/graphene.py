"""A wrapper for CloudVolumeGraphene."""
from __future__ import annotations

import warnings
from typing import Optional

import cloudvolume as cv
import provenancetoolbox as ptb
from cloudvolume.frontends.graphene import CloudVolumeGraphene

from . import rules
from .volume import register_plugin


def register() -> None:
    """Registration function for CirrusVolumeGraphene.

    See volume.register_plugin for more information.
    """
    register_plugin(CloudVolumeGraphene, CirrusVolumeGraphene)


# This is largely copied code from CirrusVolumePrecomputed. CloudVolumeGraphene
# declares no unique writing methods, but we still need to subclass
# CloudVolumeGraphene separately to support the extra methods that are
# declared.
class CirrusVolumeGraphene(CloudVolumeGraphene):
    """A wrapper for CloudVolumeGraphene.

    See cloudvolume.CloudVolumeGraphene for inherited methods and
    attributes.

    Additional attributes:
        sources: What volumes/processes were used as inputs to create this
            volume.
        motivation: The reason for creating or modifying this volume.
        process: A provenancetoolbox.Process describing the modifications
            being performed on this volume.
    """

    def __init__(
        self,
        cloudvolume: CloudVolumeGraphene,
        sources: Optional[list[str]] = None,
        motivation: Optional[str] = None,
        process: Optional[ptb.Process] = None,
    ):
        self.config = cloudvolume.config
        self.cache = cloudvolume.cache
        self.meta = cloudvolume.meta

        self.image = cloudvolume.image
        self.mesh = cloudvolume.mesh
        self.skeleton = cloudvolume.skeleton

        self.green_threads = cloudvolume.green_threads

        self.mip = cloudvolume.mip
        self.pid = cloudvolume.pid

        # CirrusVolume-specific attributes
        self.sources = sources
        self.motivation = motivation
        self.process = process

    # Overriding all methods that allow writing to the image
    # with versions that check the rules first
    def __setitem__(self, slices, img):
        self.document()

        super().__setitem__(slices, img)

    def upload_from_shared_memory(
        self, location, bbox, order="F", cutout_bbox=None
    ) -> None:
        self.document()

        super().upload_from_shared_memory(
            location, bbox, order=order, cutout_bbox=cutout_bbox
        )

    def upload_from_file(self, location, bbox, order="F", cutout_bbox=None) -> None:
        self.document()

        super().upload_from_file(location, bbox, order=order, cutout_bbox=cutout_bbox)

    def commit_provenance(self):
        self.document()

        super().commit_provenance()

    def document(self) -> None:
        """Commits the CirrusVolume documentation to the provenance file."""
        rules.check_writing_rules(self.sources, self.motivation, self.process)

        rules.documentvolume(self, self.sources, self.motivation, self.process)
