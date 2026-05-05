import PokemonSearch, { formatPokemon } from './PokemonSearch';

const SPRITE_BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon';

export default function PokemonPanel({ pokemon, onSelect, pokemonList }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
      <PokemonSearch pokemonList={pokemonList} selected={pokemon} onSelect={onSelect} />

      <div style={{
        width: 180,
        height: 180,
        border: '1px solid #ccc',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        {pokemon ? (
          <img
            src={`${SPRITE_BASE}/${pokemon.id}.png`}
            alt={pokemon.name}
            width={180}
            height={180}
            style={{ imageRendering: 'pixelated' }}
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
