
(import [pandas :as pd]
        math
)

(setv dataset (pd.read_csv "./output2.csv"))
(setv time (get dataset "time"))
(setv score (get dataset "score"))

(defn get_math_expectation[column]
    (/ (column.sum) (len column))
) 

(defn square[num]
 (* num num)
)

(defn get_dispersion[column]
    ( - (get_math_expectation (column.map square) ) (math.pow (get_math_expectation column ) 2) 
)) 

(
    print "Math Expectation on time:"
    (get_math_expectation time)
)
(
    print "Dispersion on score:"
    (get_dispersion score)
)
