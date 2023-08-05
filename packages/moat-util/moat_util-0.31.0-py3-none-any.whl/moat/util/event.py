"""
This module contains various helper functions and classes.
"""
from concurrent.futures import CancelledError

import anyio
import attr
import outcome

__all__ = ["ValueEvent"]


@attr.s
class ValueEvent:
    """A waitable value useful for inter-task synchronization,
    inspired by :class:`threading.Event`.

    An event object manages an internal value, which is initially
    unset, and a task can wait for it to become True.

    Args:
      ``scope``:  A cancelation scope that will be cancelled if/when
                  this ValueEvent is. Used for clean cancel propagation.

    Note that the value can only be read once.
    """

    event = attr.ib(factory=anyio.Event, init=False)
    value = attr.ib(default=None, init=False)
    scope = attr.ib(default=None, init=True)

    def set(self, value):
        """Set the result to return this value, and wake any waiting task."""
        self.value = outcome.Value(value)
        self.event.set()

    def set_error(self, exc):
        """Set the result to raise this exceptio, and wake any waiting task."""
        self.value = outcome.Error(exc)
        self.event.set()

    def is_set(self):
        """Check whether the event has occurred."""
        return self.value is not None

    def cancel(self):
        """Send a cancelation to the recipient.

        TODO: Trio can't do that cleanly.
        """
        if self.scope is not None:
            self.scope.cancel()
        self.set_error(CancelledError())

    async def wait(self):
        """Block until the value is set.

        If it's already set, then this method returns immediately.

        The value is not (yet) read; if it's an error, it will not be raised from here.
        """
        await self.event.wait()

    async def get(self):
        """Block until the value is set.

        If it's already set, then this method returns immediately.

        The value can only be read once.
        """
        await self.event.wait()
        return self.value.unwrap()
