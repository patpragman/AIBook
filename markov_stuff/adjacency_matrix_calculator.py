import numpy as np
from scipy.linalg import eig
from numpy.linalg import norm
import numpy.typing as npt


def calculate_final_states(adjacency_matrix: npt.ArrayLike) -> list[npt.ArrayLike]:
    """
    takes an adjacency matrix in, computes the left eigenvector with the eig function

    the eig function returns the eigenvalues and eigenvectors, so we only want the eigenvectors
    this gives us a complex
    """

    # calculate the left eigenvectors from the adjacency matrix
    v_l_unnormalized = eig(adjacency_matrix,
                           left=True,
                           right=False)[1].T

    # this has returned a matrix of eigenvectors, we want to transpose it so it's easier to iterate through it
    output = []

    for eigen_vector in v_l_unnormalized:
        # the sum of each row must be 1 for the probability function to work
        row_sum = eigen_vector.sum()
        if row_sum == 0:
            continue
        v = eigen_vector / row_sum

        # if it's a real valued eigenvector, append it to the output list
        if np.isreal(v).all():
            output.append(np.real(v))

    return output


def calculate_next_state(adjacency_matrix: npt.ArrayLike,
                         transition_model: npt.ArrayLike,
                         current_state: npt.ArrayLike) -> npt.ArrayLike:
    """
    takes the adjacency matrix, the transition model, and the current state, then returns the next state
    """

    return transition_model @ adjacency_matrix @ current_state


if __name__ == "__main__":
    test_array = np.array([
        [0.2, 0.6, 0.2],
        [0.3, 0.0, 0.7],
        [0.5, 0.0, 0.5]
    ])

    test_array_2 = np.array([
        [0.5, 0.5],
        [0.3, 0.7]
    ])

    print(calculate_final_states(test_array))
    print(calculate_final_states(test_array_2))


    test_array_3 = np.array([
        [0.8, 0.2],  # P(S_t = 1 | S_t-1) is the first column
        [0.2, 0.8]   # P(S_t = 2 | S_t-1) is the second column where S can be either state
    ])

    transition_model_1 = np.diag(np.array(
        [0.1,
         0.4]  # P(C|S_t)
    ))

    transition_model_2 = np.diag(np.array(
        [0.4,
         0.1]  # P(G|S_t)
    ))

    transition_model_3 = np.diag(np.array(
        [0.1,
         0.4]  # P(T |S_t)
    ))

    state = calculate_next_state(
        test_array_3,  # this corresponds to the adjacency matrix
        transition_model_1,  # this corresponds to the P(C | S_t)
        current_state=np.array([0.5, 0.5]).T  # this was the initial state
    )
    print(state)

    state = calculate_next_state(
        test_array_3,
        transition_model_2,
        current_state=state.T
    )
    print(state)

    state = calculate_next_state(
        test_array_3,
        transition_model_3,
        current_state=state.T
    )
    print(state)