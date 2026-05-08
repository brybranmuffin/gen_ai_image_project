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
      width: '100%',
      padding: '16px',
      boxSizing: 'border-box',
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
        style={{ width: '80%', cursor: 'pointer' }}
      />

      <button
        onClick={onGenerate}
        disabled={!canGenerate}
        style={{
          width: '60%',
          padding: '8px 0',
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
        width: '100%',
        aspectRatio: '1',
        border: '1px solid #ccc',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        boxSizing: 'border-box',
      }}>
        {isLoading ? (
          <div className="spinner" />
        ) : resultUrl ? (
          <img
            src={resultUrl}
            alt="Generated Pokémon"
            style={{ width: '100%', height: '100%', imageRendering: 'pixelated', objectFit: 'contain' }}
          />
        ) : (
          <span style={{ color: '#999', fontSize: '13px', textAlign: 'center', padding: '8px' }}>
            Select two Pokémon and hit Generate
          </span>
        )}
      </div>

      {resultUrl && !isLoading && (
        <div style={{ fontSize: '13px', textAlign: 'center', color: '#444' }}>
          Congratulations, you have discovered a new Pokémon!
        </div>
      )}
    </div>
  );
}
