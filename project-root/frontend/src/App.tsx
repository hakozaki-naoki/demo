import { useState, FormEvent } from 'react';
import type { Employee } from './types';

// スタイルは簡易的にインラインスタイルを使用します
const styles = {
  container: { maxWidth: '800px', margin: '2rem auto', fontFamily: 'sans-serif' },
  card: { border: '1px solid #ddd', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  input: { display: 'block', width: '100%', marginBottom: '1rem', padding: '0.5rem', boxSizing: 'border-box' as const },
  button: { padding: '0.5rem 1rem', background: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  table: { width: '100%', borderCollapse: 'collapse' as const, marginTop: '1rem' },
  th: { borderBottom: '2px solid #ddd', padding: '0.5rem', textAlign: 'left' as const },
  td: { borderBottom: '1px solid #eee', padding: '0.5rem' },
  error: { color: 'red', marginBottom: '1rem' },
};

function App() {
  // 状態管理
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState<string | null>(null); // Basic認証ヘッダー用
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [error, setError] = useState('');

  // ログイン処理
  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    // Basic認証用のBase64文字列を作成 (user:pass)
    const credentials = btoa(`${username}:${password}`);
    const authHeader = `Basic ${credentials}`;

    try {
      // 実際にAPIを叩いて認証確認を行う
      const response = await fetch('http://localhost:8000/api/employees', {
        method: 'GET',
        headers: {
          'Authorization': authHeader,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setToken(authHeader); // 認証成功したらトークンを保存
        setEmployees(data);   // データをセット
      } else {
        setError('ログインに失敗しました。ユーザー名またはパスワードが違います。');
      }
    } catch (err) {
      setError('サーバー接続エラーが発生しました。');
    }
  };

  // ログアウト処理
  const handleLogout = () => {
    setToken(null);
    setEmployees([]);
    setUsername('');
    setPassword('');
  };

  // --- 画面レンダリング ---

  // 1. ログイン画面
  if (!token) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h2>システムログイン</h2>
          <p>User: admin / Pass: password</p>
          {error && <p style={styles.error}>{error}</p>}
          <form onSubmit={handleLogin}>
            <label>
              ユーザー名
              <input
                type="text"
                style={styles.input}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </label>
            <label>
              パスワード
              <input
                type="password"
                style={styles.input}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            <button type="submit" style={styles.button}>ログイン</button>
          </form>
        </div>
      </div>
    );
  }

  // 2. 一覧表示画面
  return (
    <div style={styles.container}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>社員一覧</h2>
        <button onClick={handleLogout} style={{ ...styles.button, background: '#6c757d' }}>
          ログアウト
        </button>
      </div>
      
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>ID</th>
            <th style={styles.th}>名前</th>
            <th style={styles.th}>部署</th>
            <th style={styles.th}>Email</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((emp) => (
            <tr key={emp.id}>
              <td style={styles.td}>{emp.id}</td>
              <td style={styles.td}>{emp.name}</td>
              <td style={styles.td}>{emp.department}</td>
              <td style={styles.td}>{emp.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;