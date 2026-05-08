import PokemonSearch, { formatPokemon } from './PokemonSearch';

const SPRITE_BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon';

export default function PokemonPanel({ pokemon, onSelect, pokemonList }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '10px',
      width: '100%',
      padding: '16px',
      boxSizing: 'border-box',
    }}>
      <PokemonSearch pokemonList={pokemonList} selected={pokemon} onSelect={onSelect} />

      <div style={{
        width: '100%',
        aspectRatio: '1',
        border: '1px solid #ccc',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxSizing: 'border-box',
      }}>
        {pokemon ? (
          <img
            src={`${SPRITE_BASE}/${pokemon.id}.png`}
            alt={pokemon.name}
            style={{ width: '100%', height: '100%', imageRendering: 'pixelated', objectFit: 'contain' }}
          />
        ) : (
          <span style={{ color: '#999', fontSize: '13px' }}>No Pokémon selected</span>
        )}
      </div>

      <div style={{ fontSize: '14px', minHeight: '1.2em' }}>
        {pokemon ? formatPokemon(pokemon) : ''}
      </div>
    </div>
  );
}
