function displayName(pokemon) {
  if (!pokemon) return '?';
  return pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1);
}

export default function SliderPanel({
  sliderValue, setSliderValue,
  leftPokemon, rightPokemon,
  onGenerate, isLoading, resultUrl,
}) {
  const canGenerate = leftPokemon && rightPokemon && !isLoading;

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

      <button
        onClick={onGenerate}
        disabled={!canGenerate}
        style={{
          padding: '8px 24px',
          fontSize: '14px',
          cursor: canGenerate ? 'pointer' : 'not-allowed',
          opacity: canGenerate ? 1 : 0.4,
          borderRadius: '4px',
          border: '1px solid #ccc',
          background: canGenerate ? '#222' : '#ccc',
          color: canGenerate ? '#fff' : '#666',
        }}
      >
        {isLoading ? 'Generating…' : 'Generate'}
      </button>

      <div style={{
        width: 180,
        height: 180,
        border: '1px solid #ccc',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        {isLoading ? (
          <div className="spinner" />
        ) : resultUrl ? (
          <img
            src={resultUrl}
            alt="Generated Pokémon"
            width={180}
            height={180}
            style={{ imageRendering: 'pixelated' }}
          />
        ) : (
          <span style={{ color: '#999', fontSize: '13px', textAlign: 'center', padding: '8px' }}>
            Select two Pokémon and hit Generate
          </span>
        )}
      </div>

      {resultUrl && !isLoading && (
        <div style={{ fontSize: '13px', textAlign: 'center', color: '#444', maxWidth: '180px' }}>
          Congratulations, you have discovered a new Pokémon!
        </div>
      )}
    </div>
  );
}
