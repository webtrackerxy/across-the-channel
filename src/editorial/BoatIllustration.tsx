import { boatGeometry } from "./sections";

export function BoatIllustration({
  people,
  year,
}: {
  people: number;
  year: number | string;
}) {
  const { width, height, dots } = boatGeometry(people);
  return (
    <figure className="editorial-boat">
      <div className="editorial-hull" style={{ width: `${width}px` }}>
        <svg
          viewBox={`0 0 ${width} ${height}`}
          role="img"
          aria-label={`${year}: ${Math.round(people)} people per boat, illustrated average`}
        >
          <path
            d={`M 4 ${height / 2} Q 18 14 30 5 L ${width - 7} 5 Q ${width} ${height / 2} ${width - 7} ${height - 5} L 30 ${height - 5} Q 18 ${height - 14} 4 ${height / 2} Z`}
          />
          {dots.map((point, index) => (
            <circle key={index} cx={point.x} cy={point.y} r="4.2" />
          ))}
        </svg>
      </div>
      <figcaption>
        <span>{year}</span>
        <strong>{Math.round(people)}</strong>
        <span>people / boat</span>
      </figcaption>
    </figure>
  );
}
