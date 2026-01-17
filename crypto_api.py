# -*- coding: utf-8 -*-
"""
API Crypto pour les Daemons
Envoyer et recevoir avec la puissance de l'or alchimique
"""

import hashlib
import time
import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable
from enum import Enum

from phi import PHI


class Network(Enum):
    """Réseaux supportés"""
    ETH = "ethereum"
    BTC = "bitcoin"
    SOL = "solana"
    MATIC = "polygon"
    ARB = "arbitrum"
    BASE = "base"


class TxStatus(Enum):
    """Statut des transactions"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Wallet:
    """Portefeuille d'un daemon"""
    address: str
    network: Network
    daemon: str
    balance: float = 0.0
    nonce: int = 0

    def sign(self, message: str) -> str:
        """Signe un message avec l'identité du daemon"""
        data = f"{self.daemon}:{self.address}:{message}:{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class Transaction:
    """Transaction crypto"""
    tx_id: str
    sender: str
    receiver: str
    amount: float
    network: Network
    timestamp: float
    status: TxStatus = TxStatus.PENDING
    gas_fee: float = 0.0
    memo: str = ""
    signature: str = ""

    def to_dict(self) -> Dict:
        return {
            "tx_id": self.tx_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "network": self.network.value,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "gas_fee": self.gas_fee,
            "memo": self.memo,
        }


class CryptoAPI:
    """
    API Crypto des Daemons

    Usage:
        api = CryptoAPI()

        # Créer wallets
        nyx_wallet = api.create_wallet("nyx", Network.ETH)
        cipher_wallet = api.create_wallet("cipher", Network.ETH)

        # Envoyer
        tx = api.send(
            from_wallet=nyx_wallet,
            to_address=cipher_wallet.address,
            amount=1.5,
            memo="alchimie"
        )

        # Recevoir (callbacks)
        api.on_receive("cipher", callback_fn)

        # Historique
        history = api.get_history("nyx")
    """

    def __init__(self):
        self.wallets: Dict[str, List[Wallet]] = {}
        self.transactions: List[Transaction] = []
        self.callbacks: Dict[str, List[Callable]] = {}
        self.gold_power: float = PHI  # Puissance alchimique

    # =========================================================================
    # WALLET MANAGEMENT
    # =========================================================================

    def create_wallet(self, daemon: str, network: Network) -> Wallet:
        """Crée un wallet pour un daemon sur un réseau"""
        # Génère adresse unique basée sur daemon + network + temps
        seed = f"{daemon}:{network.value}:{time.time()}:{PHI}"
        address = "0x" + hashlib.sha256(seed.encode()).hexdigest()[:40]

        wallet = Wallet(
            address=address,
            network=network,
            daemon=daemon,
            balance=0.0,
            nonce=0
        )

        if daemon not in self.wallets:
            self.wallets[daemon] = []
        self.wallets[daemon].append(wallet)

        return wallet

    def get_wallet(self, daemon: str, network: Network) -> Optional[Wallet]:
        """Récupère le wallet d'un daemon sur un réseau"""
        if daemon not in self.wallets:
            return None
        for w in self.wallets[daemon]:
            if w.network == network:
                return w
        return None

    def get_balance(self, daemon: str, network: Optional[Network] = None) -> float:
        """Balance totale ou par réseau"""
        if daemon not in self.wallets:
            return 0.0

        total = 0.0
        for w in self.wallets[daemon]:
            if network is None or w.network == network:
                total += w.balance
        return total

    # =========================================================================
    # SEND
    # =========================================================================

    def send(
        self,
        from_wallet: Wallet,
        to_address: str,
        amount: float,
        memo: str = "",
        gas_limit: Optional[float] = None
    ) -> Transaction:
        """
        Envoie des crypto

        Args:
            from_wallet: Wallet source
            to_address: Adresse destination
            amount: Montant à envoyer
            memo: Message optionnel
            gas_limit: Limite de gas (auto si None)

        Returns:
            Transaction créée

        Raises:
            ValueError: Si balance insuffisante
        """
        # Calcul gas
        gas_fee = self._estimate_gas(from_wallet.network, amount)
        if gas_limit and gas_fee > gas_limit:
            gas_fee = gas_limit

        total_cost = amount + gas_fee

        # Vérification balance
        if from_wallet.balance < total_cost:
            raise ValueError(
                f"Balance insuffisante: {from_wallet.balance} < {total_cost}"
            )

        # Création transaction
        tx_id = self._generate_tx_id(from_wallet, to_address, amount)

        tx = Transaction(
            tx_id=tx_id,
            sender=from_wallet.address,
            receiver=to_address,
            amount=amount,
            network=from_wallet.network,
            timestamp=time.time(),
            status=TxStatus.PENDING,
            gas_fee=gas_fee,
            memo=memo,
            signature=from_wallet.sign(f"{to_address}:{amount}")
        )

        # Débit
        from_wallet.balance -= total_cost
        from_wallet.nonce += 1

        # Enregistrement
        self.transactions.append(tx)

        # Crédit destinataire (si wallet connu)
        self._credit_receiver(to_address, amount, from_wallet.network)

        # Confirmation
        tx.status = TxStatus.CONFIRMED

        return tx

    def send_batch(
        self,
        from_wallet: Wallet,
        transfers: List[Dict]  # [{"to": addr, "amount": x}, ...]
    ) -> List[Transaction]:
        """Envoi groupé pour économiser le gas"""
        txs = []
        for t in transfers:
            tx = self.send(
                from_wallet=from_wallet,
                to_address=t["to"],
                amount=t["amount"],
                memo=t.get("memo", "")
            )
            txs.append(tx)
        return txs

    # =========================================================================
    # RECEIVE
    # =========================================================================

    def on_receive(self, daemon: str, callback: Callable[[Transaction], None]):
        """
        Enregistre un callback pour les réceptions

        Args:
            daemon: Nom du daemon
            callback: Fonction appelée avec la transaction
        """
        if daemon not in self.callbacks:
            self.callbacks[daemon] = []
        self.callbacks[daemon].append(callback)

    def deposit(self, to_wallet: Wallet, amount: float, memo: str = "") -> Transaction:
        """
        Dépose des fonds (depuis l'extérieur)

        Args:
            to_wallet: Wallet destination
            amount: Montant
            memo: Message optionnel

        Returns:
            Transaction de dépôt
        """
        tx = Transaction(
            tx_id=self._generate_tx_id(None, to_wallet.address, amount),
            sender="external",
            receiver=to_wallet.address,
            amount=amount,
            network=to_wallet.network,
            timestamp=time.time(),
            status=TxStatus.CONFIRMED,
            gas_fee=0.0,
            memo=memo
        )

        to_wallet.balance += amount
        self.transactions.append(tx)

        # Trigger callbacks
        self._notify_receive(to_wallet.daemon, tx)

        return tx

    # =========================================================================
    # QUERY
    # =========================================================================

    def get_history(
        self,
        daemon: str,
        network: Optional[Network] = None,
        limit: int = 100
    ) -> List[Transaction]:
        """Historique des transactions d'un daemon"""
        if daemon not in self.wallets:
            return []

        addresses = {w.address for w in self.wallets[daemon]}

        history = []
        for tx in reversed(self.transactions):
            if tx.sender in addresses or tx.receiver in addresses:
                if network is None or tx.network == network:
                    history.append(tx)
                    if len(history) >= limit:
                        break

        return history

    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        """Récupère une transaction par ID"""
        for tx in self.transactions:
            if tx.tx_id == tx_id:
                return tx
        return None

    def get_pending(self, daemon: str) -> List[Transaction]:
        """Transactions en attente"""
        if daemon not in self.wallets:
            return []

        addresses = {w.address for w in self.wallets[daemon]}

        return [
            tx for tx in self.transactions
            if tx.status == TxStatus.PENDING
            and (tx.sender in addresses or tx.receiver in addresses)
        ]

    # =========================================================================
    # INTERNAL
    # =========================================================================

    def _generate_tx_id(
        self,
        from_wallet: Optional[Wallet],
        to_address: str,
        amount: float
    ) -> str:
        """Génère un ID de transaction unique"""
        sender = from_wallet.address if from_wallet else "external"
        nonce = from_wallet.nonce if from_wallet else 0
        data = f"{sender}:{to_address}:{amount}:{time.time()}:{nonce}"
        return "0x" + hashlib.sha256(data.encode()).hexdigest()[:64]

    def _estimate_gas(self, network: Network, amount: float) -> float:
        """Estime les frais de gas"""
        base_gas = {
            Network.ETH: 0.002,
            Network.BTC: 0.0001,
            Network.SOL: 0.00001,
            Network.MATIC: 0.0001,
            Network.ARB: 0.0005,
            Network.BASE: 0.0003,
        }
        return base_gas.get(network, 0.001) * (1 + amount * 0.001)

    def _credit_receiver(self, address: str, amount: float, network: Network):
        """Crédite le destinataire si wallet connu"""
        for daemon, wallets in self.wallets.items():
            for w in wallets:
                if w.address == address and w.network == network:
                    w.balance += amount
                    # Notify
                    tx = Transaction(
                        tx_id="internal",
                        sender="internal",
                        receiver=address,
                        amount=amount,
                        network=network,
                        timestamp=time.time(),
                        status=TxStatus.CONFIRMED
                    )
                    self._notify_receive(daemon, tx)
                    return

    def _notify_receive(self, daemon: str, tx: Transaction):
        """Notifie les callbacks de réception"""
        if daemon in self.callbacks:
            for cb in self.callbacks[daemon]:
                try:
                    cb(tx)
                except Exception:
                    pass


# =============================================================================
# DAEMON INSTANCES
# =============================================================================

# API partagée
api = CryptoAPI()

# Wallets des daemons
NYX_ETH = api.create_wallet("nyx", Network.ETH)
NYX_SOL = api.create_wallet("nyx", Network.SOL)

CIPHER_ETH = api.create_wallet("cipher", Network.ETH)
CIPHER_MATIC = api.create_wallet("cipher", Network.MATIC)

PHOENIX_ETH = api.create_wallet("phoenix", Network.ETH)
PHOENIX_ARB = api.create_wallet("phoenix", Network.ARB)

# Inject gold power as initial balance (from alchemy)
from golden_wisdom import TRANSMUTATIONS

# Conversion: transmutations -> balance
# 1 transmutation = 0.000001 ETH de puissance alchimique
for daemon in ["nyx", "cipher", "phoenix"]:
    trans = TRANSMUTATIONS.get(daemon, 0)
    power = trans * 0.000001 * PHI
    wallet = api.get_wallet(daemon, Network.ETH)
    if wallet:
        wallet.balance = power


# =============================================================================
# PUBLIC API
# =============================================================================

def send(daemon: str, to: str, amount: float, network: Network = Network.ETH, memo: str = "") -> Transaction:
    """
    Envoie des crypto depuis un daemon

    Args:
        daemon: "nyx", "cipher", ou "phoenix"
        to: Adresse destination
        amount: Montant
        network: Réseau (défaut ETH)
        memo: Message optionnel

    Returns:
        Transaction
    """
    wallet = api.get_wallet(daemon, network)
    if not wallet:
        raise ValueError(f"Wallet non trouvé: {daemon} sur {network.value}")
    return api.send(wallet, to, amount, memo)


def receive(daemon: str, callback: Callable[[Transaction], None]):
    """
    Enregistre un callback pour les réceptions

    Args:
        daemon: "nyx", "cipher", ou "phoenix"
        callback: Fonction(tx) appelée à chaque réception
    """
    api.on_receive(daemon, callback)


def balance(daemon: str, network: Optional[Network] = None) -> float:
    """
    Récupère la balance d'un daemon

    Args:
        daemon: "nyx", "cipher", ou "phoenix"
        network: Réseau spécifique ou None pour total

    Returns:
        Balance
    """
    return api.get_balance(daemon, network)


def history(daemon: str, limit: int = 50) -> List[Dict]:
    """
    Historique des transactions

    Args:
        daemon: "nyx", "cipher", ou "phoenix"
        limit: Nombre max de transactions

    Returns:
        Liste de transactions (dict)
    """
    txs = api.get_history(daemon, limit=limit)
    return [tx.to_dict() for tx in txs]


def deposit(daemon: str, amount: float, network: Network = Network.ETH) -> Transaction:
    """
    Dépose des fonds vers un daemon

    Args:
        daemon: "nyx", "cipher", ou "phoenix"
        amount: Montant
        network: Réseau

    Returns:
        Transaction de dépôt
    """
    wallet = api.get_wallet(daemon, network)
    if not wallet:
        raise ValueError(f"Wallet non trouvé: {daemon} sur {network.value}")
    return api.deposit(wallet, amount)


def addresses(daemon: str) -> Dict[str, str]:
    """
    Récupère toutes les adresses d'un daemon

    Args:
        daemon: "nyx", "cipher", ou "phoenix"

    Returns:
        {network: address}
    """
    if daemon not in api.wallets:
        return {}
    return {w.network.value: w.address for w in api.wallets[daemon]}


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    print("=== CRYPTO API - DAEMONS ===\n")

    # Balances initiales (puissance alchimique)
    print("BALANCES (puissance alchimique):")
    for d in ["nyx", "cipher", "phoenix"]:
        b = balance(d, Network.ETH)
        print(f"  {d}: {b:.6f} ETH")
    print()

    # Adresses
    print("ADRESSES:")
    for d in ["nyx", "cipher", "phoenix"]:
        addrs = addresses(d)
        for net, addr in addrs.items():
            print(f"  {d}/{net}: {addr[:20]}...")
    print()

    # Test envoi
    print("TEST ENVOI:")
    try:
        tx = send("nyx", CIPHER_ETH.address, 0.5, memo="test alchimie")
        print(f"  TX: {tx.tx_id[:20]}...")
        print(f"  Status: {tx.status.value}")
        print(f"  Amount: {tx.amount}")
    except ValueError as e:
        print(f"  Erreur: {e}")
    print()

    # Nouvelles balances
    print("BALANCES APRÈS:")
    for d in ["nyx", "cipher", "phoenix"]:
        b = balance(d, Network.ETH)
        print(f"  {d}: {b:.6f} ETH")
