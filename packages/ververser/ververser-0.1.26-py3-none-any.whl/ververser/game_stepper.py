from ververser.timer import Timer


class GameStepper:

    def __init__( self, frame_time, max_catchup_updates : int, continuous_catchup : bool ):
        self.frame_time = frame_time
        self.max_updates = 1 + max_catchup_updates
        self.continuous_catchup = continuous_catchup

        self.update_timer = Timer()
        self.remaining_time_to_consume = 0
        self.n_updates = 0

    def produce( self ) -> None:
        # measure the time that has passed since last frame,
        # this is basically time that we have to consume by running game updates
        dt = self.update_timer.restart()
        self.remaining_time_to_consume += dt
        self.n_updates = 0

    def consume( self ) -> bool:
        # consume time by running game updates
        # we choose to use fixed size timesteps because they result in more stable physics
        # you want to limit the number of consecutive updates in case you used a breakpoint,
        # and to prevent situations where your application might otherwise never catch up.
        # In a next update the app might still try to catch up to a delay from a previous update though.
        # this will result in your app temporarily responding slowly to input events, and perhaps lower framerate
        # If issues are not temporary but consistent, your target fps is probably too high,
        # (or your performance too bad...)
        has_time_to_consume = self.remaining_time_to_consume >= self.frame_time
        has_steps_to_consume = self.n_updates < self.max_updates
        can_step = has_time_to_consume and has_steps_to_consume
        if can_step:
            self.remaining_time_to_consume -= self.frame_time
            self.n_updates += 1
            return True
        if not self.continuous_catchup and self.n_updates == self.max_updates:
            self.remaining_time_to_consume = 0
        return False
