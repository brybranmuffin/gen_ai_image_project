import { useState } from 'react';
import { usePokemonList } from './usePokemonList';
import PokemonPanel from './PokemonPanel';
import SliderPanel from './SliderPanel';

export default function App() {
  const [leftPokemon, setLeftPokemon] = useState(null);
  const [rightPokemon, setRightPokemon] = useState(null);
  const [sliderValue, setSliderValue] = useState(50);
  const pokemonList = usePokemonList();

  return (
    <div style={{ padding: '24px 32px' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '32px' }}>PokAE Machine</h1>

      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr auto 1fr',
        gap: '16px',
        alignItems: 'start',
      }}>
        <PokemonPanel
          pokemon={leftPokemon}
          onSelect={setLeftPokemon}
          pokemonList={pokemonList}
        />

        <SliderPanel
          sliderValue={sliderValue}
          setSliderValue={setSliderValue}
          leftPokemon={leftPokemon}
          rightPokemon={rightPokemon}
        />

        <PokemonPanel
          pokemon={rightPokemon}
          onSelect={setRightPokemon}
          pokemonList={pokemonList}
        />
      </div>
      <footer style={{ marginTop: '48px', textAlign: 'center', fontSize: '13px', color: '#999' }}>
        Pokémon data and sprites provided by{' '}
        <a href="https://pokeapi.co" target="_blank" rel="noreferrer" style={{ color: '#999' }}>
          PokéAPI
        </a>
        {' '}— used under the{' '}
        <a href="https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md" target="_blank" rel="noreferrer" style={{ color: '#999' }}>
          BSD licence
        </a>.
      </footer>
    </div>
  );
}
