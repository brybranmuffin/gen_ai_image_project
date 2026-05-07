import { useState, useRef } from 'react';
import { usePokemonList } from './usePokemonList';
import PokemonPanel from './PokemonPanel';
import SliderPanel from './SliderPanel';

const APIM_URL = 'https://pokae-api.azure-api.net/interpolate';
const APIM_KEY = import.meta.env.VITE_APIM_KEY ?? '';

export default function App() {
  const [leftPokemon, setLeftPokemon] = useState({ id: 25, name: "pikachu" });
  const [rightPokemon, setRightPokemon] = useState({ id: 133, name: "eevee" });
  const [sliderValue, setSliderValue] = useState(50);
  const [resultUrl, setResultUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const pokemonList = usePokemonList();
  const prevUrlRef = useRef(null);

  async function handleGenerate() {
    if (!leftPokemon || !rightPokemon) return;
    setIsLoading(true);
    try {
      const alpha = sliderValue / 100;
      const url = `${APIM_URL}?pokedex_id_1=${leftPokemon.id}&pokedex_id_2=${rightPokemon.id}&alpha=${alpha}`;
      const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Ocp-Apim-Subscription-Key': APIM_KEY },
      });
      if (!resp.ok) throw new Error(`API error ${resp.status}`);
      const blob = await resp.blob();
      const newUrl = URL.createObjectURL(blob);
      if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current);
      prevUrlRef.current = newUrl;
      setResultUrl(newUrl);
    } catch (err) {
      console.error('Generation failed:', err);
    } finally {
      setIsLoading(false);
    }
  }

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
          onGenerate={handleGenerate}
          isLoading={isLoading}
          resultUrl={resultUrl}
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
