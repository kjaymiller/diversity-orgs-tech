import PropTypes from "prop-types";
import React from "react";

import { FacetValue } from "@elastic/react-search-ui-views/lib/types";
import { appendClassName } from "@elastic/react-search-ui-views/lib/view-helpers";

function getFilterValueDisplay(filterValue) {
  if ([undefined, null, ''].includes(filterValue)) {
      console.log(filterValue)
      return "N/A";
  }
  if (filterValue.hasOwnProperty("name")) return filterValue.name;
  return String(filterValue);
}

function _MultiCheckboxFacet({
  className,
  label,
  onMoreClick,
  onRemove,
  onSelect,
  options,
  showMore,
  showSearch,
  onSearch,
  searchPlaceholder
}) {
  return (
    <fieldset className={appendClassName("sui-facet", className)}>
      <div className="xl:flex-1 items-center justify-around px-3 text-lg">
        {options.length < 1 && <div>No matching options</div>}
        {options.map(option => {
          return (
            <label
              className="m-3"
              key={`${getFilterValueDisplay(option.value)}`}
              htmlFor={`example_facet_${label}${getFilterValueDisplay(
                option.value
              )}`}
            >
              <button 
              className="border hover:text-gray-100 focus:text-gray-100 hover:font-bold focus:font-bold bg-gradient-to-br focus:to-blue-200 focus:from-indigo-500  hover:to-blue-200 hover:from-indigo-500  p-3 border-ingigo-200 my-4 rounded-lg"
              onClick={() =>
                    onSelect(option.value)
                  }
              >
                  {getFilterValueDisplay(option.value)}

              </button>
            </label>
          );
        })}
      <button 
      onClick = {() => 
        onRemove(options.value)
      }
      className="text-sm h-1/3 rounded-xl p-2 border bg-gradient-to-br hover:from-pink-500 hover:to-red-200 from-gray-300"
      >Reset</button>
      </div>

      {showMore && (
        <button
          type="button"
          className=""
          onClick={onMoreClick}
          aria-label="Show more options"
        >
          + More
        </button>
      )}
    </fieldset>
  );
}

_MultiCheckboxFacet.propTypes = {
  label: PropTypes.string.isRequired,
  onMoreClick: PropTypes.func.isRequired,
  onRemove: PropTypes.func.isRequired,
  onSelect: PropTypes.func.isRequired,
  onSearch: PropTypes.func.isRequired,
  options: PropTypes.arrayOf(FacetValue).isRequired,
  showMore: PropTypes.bool.isRequired,
  className: PropTypes.string,
  showSearch: PropTypes.bool,
  searchPlaceholder: PropTypes.string
};

export default _MultiCheckboxFacet;
