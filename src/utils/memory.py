"""Gerenciador de memória para assistentes"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class MemoryManager:
    """Gerenciador de memória persistente para assistentes."""
    
    def __init__(self, storage_path: str = "storage/memory"):
        """
        Inicializa o gerenciador de memória.
        
        Args:
            storage_path: Caminho para armazenar os arquivos de memória
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memories: Dict[str, Any] = {}
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._load_memories()
    
    def _get_memory_file(self, user_id: str = "default") -> Path:
        """Retorna o caminho do arquivo de memória para um usuário."""
        return self.storage_path / f"{user_id}_memory.json"
    
    def _load_memories(self, user_id: str = "default"):
        """Carrega memórias do arquivo."""
        memory_file = self._get_memory_file(user_id)
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    self.memories = json.load(f)
            except json.JSONDecodeError:
                self.memories = {}
        else:
            self.memories = {}
    
    def _save_memories(self, user_id: str = "default"):
        """Salva memórias no arquivo."""
        memory_file = self._get_memory_file(user_id)
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def remember(self, key: str, value: Any, user_id: str = "default"):
        """
        Armazena uma informação na memória.
        
        Args:
            key: Chave da memória
            value: Valor a ser armazenado
            user_id: ID do usuário
        """
        if user_id not in self.memories:
            self.memories[user_id] = {}
        
        self.memories[user_id][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.current_session_id
        }
        
        self._save_memories(user_id)
    
    def recall(self, key: str, user_id: str = "default") -> Optional[Any]:
        """
        Recupera uma informação da memória.
        
        Args:
            key: Chave da memória
            user_id: ID do usuário
            
        Returns:
            Valor armazenado ou None se não existir
        """
        if user_id in self.memories and key in self.memories[user_id]:
            return self.memories[user_id][key].get("value")
        return None
    
    def get_all_memories(self, user_id: str = "default") -> Dict[str, Any]:
        """
        Retorna todas as memórias de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com todas as memórias
        """
        return self.memories.get(user_id, {})
    
    def clear_memories(self, user_id: str = "default"):
        """
        Limpa todas as memórias de um usuário.
        
        Args:
            user_id: ID do usuário
        """
        if user_id in self.memories:
            self.memories[user_id] = {}
            self._save_memories(user_id)
    
    def get_context_summary(self, user_id: str = "default", limit: int = 10) -> str:
        """
        Retorna um resumo das memórias recentes para contexto.
        
        Args:
            user_id: ID do usuário
            limit: Número máximo de memórias a incluir
            
        Returns:
            String com resumo das memórias
        """
        user_memories = self.get_all_memories(user_id)
        if not user_memories:
            return "Nenhuma memória anterior encontrada."
        
        # Ordenar por timestamp
        sorted_memories = sorted(
            user_memories.items(),
            key=lambda x: x[1].get("timestamp", ""),
            reverse=True
        )[:limit]
        
        summary = "📝 Memórias anteriores:\n"
        for key, data in sorted_memories:
            value = data.get("value", "")
            timestamp = data.get("timestamp", "")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%d/%m %H:%M")
                    summary += f"• [{time_str}] {key}: {value}\n"
                except:
                    summary += f"• {key}: {value}\n"
            else:
                summary += f"• {key}: {value}\n"
        
        return summary