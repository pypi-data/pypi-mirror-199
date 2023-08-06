export default function existsOrValue(
  object: {},
  property: string,
  value: string | {}
) {
  return object && property in object ? object[property] : value;
}
