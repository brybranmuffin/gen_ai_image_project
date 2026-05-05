function displayName(pokemon) {
  if (!pokemon) return '?';
  return pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1);
}

export default function SliderPanel({ sliderValue, setSliderValue, leftPokemon, rightPokemon }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '12px',
      padding: '0 24px',
    }}>
      <div style={{ textAlign: 'center', lineHeight: '1.6', fontSize: '15px' }}>
        <div>{sliderValue}% {displayName(leftPokemon)}</div>
        <div>{100 - sliderValue}% {displayName(rightPokemon)}</div>
      </div>

      <input
        type="range"
        min="1"
        max="99"
        step="1"
        value={sliderValue}
        onChange={e => setSliderValue(Number(e.target.value))}
        style={{ width: '180px', cursor: 'pointer' }}
      />
    </div>
  );
}
