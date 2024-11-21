const usernameRegex = /^[a-zA-Z\d_-]{1,20}$/; // 英数字、アンダースコア、ハイフンを許可
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const passwordRegex =
  /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*_-])[a-zA-z\d!@#$%^&*_-]{8,20}$/; // 英数字と記号（!@#$%^&*_-）を含む

const isValidUsername = (username) => usernameRegex.test(username);
const isValidEmail = (email) => emailRegex.test(email);
const isValidPassword = (password) => passwordRegex.test(password);

const validateInput = (username, email, password) => {
  if (username && !isValidUsername(username)) {
    return "ユーザー名は20文字以内で、英数字またはアンダースコア、ハイフンを使用してください";
  }
  if (email && !isValidEmail(email)) {
    return "メールアドレスの形式が正しくありません";
  }
  if (password && !isValidPassword(password)) {
    return "パスワードは8～20文字で、英数字と記号（!@#$%^&*_-）を含む必要があります";
  }
  return;
};

export { validateInput };
