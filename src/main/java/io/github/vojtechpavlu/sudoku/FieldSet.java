package io.github.vojtechpavlu.sudoku;


import java.util.List;


/**
 * <i>AUTHOR OF THIS PROJECT IS NOT RESPONSIBLE FOR ANY DAMAGE TO
 * THE USER'S DEVICE CAUSED BY USING THIS SOFTWARE, NO DATA LEAKS
 * OR DATA INTEGRITY DAMAGE.</i>
 *
 * <i>THIS PIECE OF SOFTWARE WAS MADE WITH NO GUARANTEE AND SHOULD
 * NOT BE USED FOR CRITICAL INFRASTRUCTURE OF YOUR APPS. THIS
 * PROJECT WAS CREATED JUST FOR FUN.</i>
 *
 *
 * <p>Interface of {@link FieldSet} defines a basic set of signatures
 * of methods overridden by it's descendants.</p>
 *
 *
 * <p></p>
 *
 * @author Vojtech Pavlu
 * @version 2021-03-29
 */
public interface FieldSet {

    /**
     * <p>Returns a boolean state if the {@link FieldSet} is consistent or not.</p>
     *
     * @return  returns a {@code boolean} information about the consistency
     *          of the set. Returns {@code true} when the current state does
     *          not violate any of the rules of the game.
     */
    public boolean isConsistent();


    /**
     * <p>Returns a boolean state about the completeness of the set.</p>
     *
     * @return  {@code true} only if the set contains complete fields only.
     */
    public boolean isComplete();


    /**
     * <p>Returns all the fields with not completed value.</p>
     *
     * @return  {@link List} of incomplete (not finished) {@link Field}s.
     */
    public List<Field> getIncomplete();



}
