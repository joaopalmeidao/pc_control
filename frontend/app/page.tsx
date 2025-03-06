"use client";

import { useState, useEffect } from "react";
import { Slider } from "@mui/material";

const API_URL = "http://localhost:5000";

export function Card({ children }: { children: React.ReactNode }) {
  return <div className="w-96 p-4 shadow-md bg-white rounded-lg p-4">{children}</div>;
}

export default function PcControl() {
  const [brightness, setBrightness] = useState<number>(50);
  const [volume, setVolume] = useState<number>(50);

  useEffect(() => {
    fetch(`${API_URL}/get_brightness`)
      .then((res) => res.json())
      .then((data) => setBrightness(data.brightness))
      .catch((err) => console.error("Erro ao obter brilho:", err));

    fetch(`${API_URL}/get_volume`)
      .then((res) => res.json())
      .then((data) => setVolume(data.volume))
      .catch((err) => console.error("Erro ao obter volume:", err));
  }, []);

  const handleBrightnessChange = (_: Event, newValue: number) => {
    const value = Array.isArray(newValue) ? newValue[0] : newValue;
    setBrightness(newValue);
    fetch(`${API_URL}/set_brightness`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ level: value }),
    }).catch((err) => console.error("Erro ao definir brilho:", err));
  };

  const handleVolumeChange = (_: Event, newValue: number) => {
    setVolume(newValue);
    fetch(`${API_URL}/set_volume`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ level: newValue }),
    }).catch((err) => console.error("Erro ao definir volume:", err));
  };

  return (
    <div className="flex flex-col items-center gap-6 p-6 min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold text-gray-800">Controle do PC</h1>
      <Card>
        <h2 className="text-lg font-semibold mb-2 text-gray-700">Controle de Brilho</h2>
        <Slider value={brightness} onChange={handleBrightnessChange} min={0} max={100} />
        <p className="text-center mt-2 text-gray-600">{brightness}%</p>
      </Card>
      
      <Card>
        <h2 className="text-lg font-semibold mb-2 text-gray-700">Controle de Volume</h2>
        <Slider value={volume} onChange={handleVolumeChange} min={0} max={100} />
        <p className="text-center mt-2 text-gray-600">{volume}%</p>
      </Card>
    </div>
  );
}