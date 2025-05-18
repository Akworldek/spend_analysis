import React, { useState, useEffect } from 'react';
import './App.css';
import { API_ENDPOINTS } from './config/api';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch transactions when component mounts
    const fetchTransactions = async () => {
      try {
        setLoading(true);
        const response = await fetch(API_ENDPOINTS.TRANSACTIONS);
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        setTransactions(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching transactions:", error);
        setError("Failed to load transactions. Please try again later.");
        setLoading(false);
      }
    };

    fetchTransactions();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Spend Analysis Dashboard</h1>
      </header>
      
      <main className="App-main">
        {loading ? (
          <p>Loading transactions...</p>
        ) : error ? (
          <div className="error-message">
            <p>{error}</p>
            <p>Note: Make sure your Django backend is running at http://localhost:8000</p>
          </div>
        ) : (
          <div className="transactions-container">
            <h2>Recent Transactions</h2>
            {transactions.length === 0 ? (
              <p>No transactions found. Add some transactions to get started!</p>
            ) : (
              <ul className="transactions-list">
                {transactions.map((transaction) => (
                  <li key={transaction.id} className="transaction-item">
                    <div className="transaction-amount">${transaction.amount.toFixed(2)}</div>
                    <div className="transaction-details">
                      <h3>{transaction.description}</h3>
                      <p>Category: {transaction.category}</p>
                      <p>Date: {new Date(transaction.date).toLocaleDateString()}</p>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </main>
      
      <footer className="App-footer">
        <p>Spend Analysis App &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;