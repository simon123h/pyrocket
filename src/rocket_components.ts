import { Poly } from "./objects";

/** Rocket part base class. */
export class RocketPart extends Poly {}
/** Fuel tank component. */
export class FuelTank extends RocketPart {}
/** Jet engine component. */
export class JeEngine extends RocketPart {}
/** Booster component. */
export class Booster extends RocketPart {}
/** Nose cone component. */
export class NoseCone extends RocketPart {}
/** Fins component. */
export class Fins extends RocketPart {}
/** Reaction wheel component. */
export class ReactionWheel extends RocketPart {}
/** Air brakes component. */
export class AirBrakes extends RocketPart {}
/** Parachute component. */
export class Parachute extends RocketPart {}
