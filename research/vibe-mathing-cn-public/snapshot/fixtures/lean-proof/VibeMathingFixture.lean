import Mathlib.Data.Nat.Basic

namespace VibeMathingFixture

/-- 固定的最小算术陈述，用于证明 kernel 与 axiom 审计链真实可运行。 -/
theorem two_add_two : (2 : ℕ) + 2 = 4 := by
  rfl

#print axioms two_add_two

end VibeMathingFixture
